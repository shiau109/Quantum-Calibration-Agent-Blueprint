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

"""Cross-platform process liveness and termination.

POSIX-only idioms (os.kill(pid, 0) probes, /proc scraping, os.killpg) are
not portable: on Windows, os.kill with any signal other than CTRL_C_EVENT /
CTRL_BREAK_EVENT calls TerminateProcess — a liveness *probe* built on it
kills the process it is checking. Everything here goes through psutil
instead.
"""

import psutil


def is_running(pid: int) -> bool:
    """Report whether a process exists and is not a zombie.

    Never signals the process, so it is safe as a probe on every platform.
    """
    try:
        return psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
    except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
        # AccessDenied means the pid exists but belongs to another user;
        # for workflow bookkeeping that pid is not one of ours anymore.
        return False


def terminate_tree(pid: int, timeout: float = 5.0) -> None:
    """Terminate a process and all its descendants, children first.

    Sends terminate (SIGTERM / Windows TerminateProcess) to the whole tree,
    waits up to `timeout` seconds, then force-kills survivors. Missing
    processes are ignored — termination is idempotent.
    """
    try:
        root = psutil.Process(pid)
    except (psutil.NoSuchProcess, ValueError):
        return

    try:
        procs = root.children(recursive=True) + [root]
    except psutil.NoSuchProcess:
        procs = [root]

    for proc in procs:
        try:
            proc.terminate()
        except psutil.NoSuchProcess:
            pass

    _, alive = psutil.wait_procs(procs, timeout=timeout)
    for proc in alive:
        try:
            proc.kill()
        except psutil.NoSuchProcess:
            pass
