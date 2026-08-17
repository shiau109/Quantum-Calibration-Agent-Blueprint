# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Portability tests for the subprocess runner.

These drive core.runner.run_experiment against throwaway fixture scripts
written into tmp_path, covering the failure modes that used to be
Windows-only: backslash paths inside the generated -c bootstrap, pipe
deadlocks on large stdout, select() on pipes, and timeout handling.
"""

import json
import time

import psutil
import pytest

from core import procutil
from core.runner import run_experiment, _parse_and_validate_result


def _write_script(tmp_path, name, body):
    scripts_dir = tmp_path / "scripts with spaces"
    scripts_dir.mkdir(exist_ok=True)
    (scripts_dir / f"{name}.py").write_text(body, encoding="utf-8")
    return scripts_dir


class TestBootstrapPaths:
    def test_windows_path_with_spaces(self, tmp_path):
        """The generated -c code must survive backslashes and spaces."""
        scripts_dir = _write_script(
            tmp_path,
            "spacey",
            '''
def spacey(x: float = 1.0) -> dict:
    """Echo experiment."""
    return {"status": "success", "results": {"x": x}}
''',
        )
        result = run_experiment("spacey", {"x": 2.5}, scripts_dir)
        assert result["status"] == "success"
        assert result["results"]["x"] == 2.5

    def test_bare_sibling_import(self, tmp_path):
        """Scripts import private sibling modules without a package prefix."""
        scripts_dir = _write_script(
            tmp_path,
            "importer",
            '''
from _shared_helper import shared_value

def importer(x: float = 1.0) -> dict:
    """Uses a bare sibling import."""
    return {"status": "success", "results": {"value": shared_value()}}
''',
        )
        (scripts_dir / "_shared_helper.py").write_text(
            "def shared_value():\n    return 42\n", encoding="utf-8"
        )
        result = run_experiment("importer", {}, scripts_dir)
        assert result["results"]["value"] == 42


class TestPipeHandling:
    def test_large_stdout_no_deadlock(self, tmp_path):
        """>1MB of stdout (base64 plots) must not deadlock the pipes."""
        scripts_dir = _write_script(
            tmp_path,
            "bigout",
            '''
def bigout(n: int = 1) -> dict:
    """Emits a large payload."""
    return {"status": "success", "results": {}, "plots": [
        {"name": "big", "format": "base64", "data": "A" * (1024 * 1024)}
    ]}
''',
        )
        result = run_experiment("bigout", {}, scripts_dir, timeout=60)
        assert result["status"] == "success"
        assert len(result["plots"][0]["data"]) == 1024 * 1024

    def test_live_log_tailing(self, tmp_path):
        """stderr reaches the log file while the child is still running."""
        scripts_dir = _write_script(
            tmp_path,
            "slowlog",
            '''
import sys, time

def slowlog(x: float = 1.0) -> dict:
    """Logs then sleeps."""
    print("progress marker", file=sys.stderr, flush=True)
    time.sleep(3)
    return {"status": "success", "results": {}}
''',
        )
        log_file = tmp_path / "logs" / "output.log"

        import threading

        seen_live = threading.Event()

        def watch():
            deadline = time.time() + 10
            while time.time() < deadline:
                if log_file.exists() and "progress marker" in log_file.read_text(
                    encoding="utf-8"
                ):
                    seen_live.set()
                    return
                time.sleep(0.1)

        watcher = threading.Thread(target=watch, daemon=True)
        watcher.start()
        result = run_experiment("slowlog", {}, scripts_dir, timeout=30, log_file=log_file)
        watcher.join(timeout=1)
        assert result["status"] == "success"
        assert seen_live.is_set(), "log line only appeared after the child exited"


class TestTimeoutPolicies:
    def test_kill_policy_reaps_grandchildren(self, tmp_path, monkeypatch):
        """Timeout with kill policy terminates the whole process tree."""
        monkeypatch.setenv("SCQO_AGENT_TIMEOUT_POLICY", "kill")
        scripts_dir = _write_script(
            tmp_path,
            "spawner",
            '''
import json, subprocess, sys, time
from pathlib import Path

def spawner(pid_file: str = "") -> dict:
    """Spawns a grandchild then hangs."""
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
    Path(pid_file).write_text(str(child.pid))
    time.sleep(600)
    return {"status": "success", "results": {}}
''',
        )
        pid_file = tmp_path / "grandchild.pid"
        with pytest.raises(TimeoutError):
            run_experiment(
                "spawner", {"pid_file": str(pid_file)}, scripts_dir, timeout=5
            )
        deadline = time.time() + 10
        grandchild_pid = int(pid_file.read_text())
        while time.time() < deadline and procutil.is_running(grandchild_pid):
            time.sleep(0.2)
        assert not procutil.is_running(grandchild_pid), "grandchild survived kill"

    def test_detach_policy_leaves_child_running(self, tmp_path, monkeypatch):
        """Timeout with detach policy returns failed but does not kill."""
        monkeypatch.setenv("SCQO_AGENT_TIMEOUT_POLICY", "detach")
        scripts_dir = _write_script(
            tmp_path,
            "longhaul",
            '''
import time

def longhaul(x: float = 1.0) -> dict:
    """Runs longer than the timeout."""
    time.sleep(15)
    return {"status": "success", "results": {}}
''',
        )
        result = run_experiment("longhaul", {}, scripts_dir, timeout=2)
        assert result["status"] == "failed"
        assert "detach" in result["error"]
        pid = result["results"]["detached_pid"]
        assert procutil.is_running(pid), "detach policy must not kill the child"
        # Clean up so the test process tree stays tidy.
        procutil.terminate_tree(pid)


class TestResultParsing:
    def test_last_line_json_fallback(self):
        """Garbage before the result line is tolerated."""
        stdout = 'warming up\nnot json {\n{"status": "success", "results": {"a": 1}}\n'
        result = _parse_and_validate_result(stdout)
        assert result["status"] == "success"
        assert result["results"]["a"] == 1

    def test_no_json_still_fails(self):
        with pytest.raises(RuntimeError, match="Failed to parse"):
            _parse_and_validate_result("no json here at all\n")

    def test_unicode_result_roundtrip(self, tmp_path):
        """Non-ASCII in results survives the pipe on any console codepage."""
        scripts_dir = _write_script(
            tmp_path,
            "unicody",
            '''
def unicody(x: float = 1.0) -> dict:
    """Returns unicode."""
    return {"status": "success", "results": {"note": "T1 = 29.9 \\u00b5s"}}
''',
        )
        result = run_experiment("unicody", {}, scripts_dir)
        assert result["results"]["note"] == "T1 = 29.9 µs"


class TestProcutil:
    def test_is_running_does_not_kill(self):
        """The liveness probe must never terminate what it checks."""
        import subprocess
        import sys

        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
        try:
            assert procutil.is_running(child.pid) is True
            time.sleep(0.5)
            assert child.poll() is None, "probe killed the process"
        finally:
            procutil.terminate_tree(child.pid)

    def test_is_running_false_for_dead(self):
        import subprocess
        import sys

        child = subprocess.Popen([sys.executable, "-c", "pass"])
        child.wait()
        # A wait()ed child is fully reaped on Windows and a zombie on POSIX;
        # both must read as not running.
        assert procutil.is_running(child.pid) is False or psutil.pid_exists(
            child.pid
        ) is False
