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

"""Subprocess experiment execution."""

import json
import os
import subprocess
import sys
import threading
from copy import deepcopy
from pathlib import Path

import numpy as np

from .discovery import get_experiment_schema
from .models import ExperimentSchema, ParameterSpec
from .procutil import terminate_tree


def resolve_params(params: dict, schema: ExperimentSchema) -> dict:
    """Merge parameter overrides with defaults discovery safely resolved.

    A default is only carried over when validation would accept it. Discovery
    records an annotation name verbatim when it is not one of the few it maps,
    so a signature like `Dict[str, int]` yields the type name "Dict", which
    _check_type does not recognise. Injecting such a default would fail
    validation and abort a run that previously worked, because the parameter
    used to be omitted and Python applied the declared default itself. Leaving
    it out preserves that behaviour.
    """
    effective_params = {
        param.name: deepcopy(param.default)
        for param in schema.parameters
        if not param.required
        and param.default_resolved
        and not _check_value(param, param.default)
    }
    effective_params.update(params)
    return effective_params


def _check_value(spec: ParameterSpec, value: any) -> list[str]:
    """Return the validation errors for one parameter value.

    Shared by validate_params and resolve_params so that the rules deciding
    whether a value is acceptable live in exactly one place.
    """
    errors = []

    if (
        value is None
        and not spec.required
        and spec.default_resolved
        and spec.default is None
    ):
        return errors

    # Check type (strict, no coercion)
    if not _check_type(value, spec.type):
        errors.append(
            f"Parameter {spec.name} has wrong type. "
            f"Expected {spec.type}, got {type(value).__name__}"
        )
        return errors

    # Check range for numeric types
    if spec.range and spec.type in ("int", "float"):
        min_val, max_val = spec.range
        # An open bound is recorded as None, because the infinity that would
        # otherwise express it is not portable JSON.
        #
        # Each side is negated rather than compared directly so that NaN,
        # which returns false for every comparison, still fails the check
        # instead of silently satisfying both sides.
        below = min_val is not None and not (value >= min_val)
        above = max_val is not None and not (value <= max_val)
        if below or above:
            errors.append(
                f"Parameter {spec.name} out of range. "
                f"Expected [{min_val}, {max_val}], got {value}"
            )

    return errors


def validate_params(params: dict, schema: ExperimentSchema) -> list[str]:
    """Validate parameters against experiment schema.

    Args:
        params: Parameter dictionary to validate
        schema: Experiment schema with parameter specifications

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Build lookup for parameter specs
    param_specs = {p.name: p for p in schema.parameters}

    # Check for required parameters
    for param_spec in schema.parameters:
        if param_spec.required and param_spec.name not in params:
            errors.append(f"Missing required parameter: {param_spec.name}")

    # Validate provided parameters
    for param_name, param_value in params.items():
        # Check if parameter exists in schema
        if param_name not in param_specs:
            errors.append(f"Unknown parameter: {param_name}")
            continue

        errors.extend(_check_value(param_specs[param_name], param_value))

    return errors


def run_experiment(
    name: str,
    params: dict,
    scripts_dir: Path,
    timeout: int = 300,
    python_path: str = None,
    log_file: Path = None,
    extra_env: dict = None,
) -> dict:
    """Run an experiment in a subprocess.

    Args:
        name: Experiment name (function name)
        params: Parameters to pass to experiment
        scripts_dir: Directory containing experiment scripts
        timeout: Timeout in seconds (default 300)
        python_path: Path to Python interpreter (default: sys.executable)
        log_file: Optional path to write progress output (stderr) in real-time
        extra_env: Optional environment variables merged over the parent's
            for the child process (e.g. provenance ids)

    Returns:
        Result dictionary with status, results, arrays, plots, metadata

    Raises:
        ValueError: If experiment not found or validation fails
        RuntimeError: If subprocess execution fails
        TimeoutError: If experiment exceeds timeout and the timeout policy
            is "kill" (with SCQO_AGENT_TIMEOUT_POLICY=detach a synthesized
            failed result is returned instead and the child keeps running)
    """
    # Get experiment schema
    schema = get_experiment_schema(name, scripts_dir)
    if schema is None:
        raise ValueError(f"Experiment not found: {name}")

    # Resolve only defaults that discovery can safely carry over JSON. Dynamic
    # defaults remain omitted so Python applies their real declared values.
    params = resolve_params(params, schema)

    validation_errors = validate_params(params, schema)
    if validation_errors:
        raise ValueError(f"Parameter validation failed: {'; '.join(validation_errors)}")

    # Get module name from script path
    module_path = Path(schema.module_path)
    module_name = module_path.stem

    # Build subprocess command: Python code passed to -c that imports the
    # function and calls it. Paths are embedded as repr'd POSIX strings —
    # raw Windows paths inside quoted literals are backslash escapes
    # (C:\Users -> \U -> SyntaxError in the child).
    #
    # scripts_dir's parent makes the package-qualified import work; scripts_dir
    # itself makes the scripts' own bare imports (e.g. `from _scqo_runtime
    # import ...`) resolve regardless of the child's working directory.
    scripts_dir_resolved = Path(scripts_dir).resolve()
    scripts_parent = scripts_dir_resolved.parent.as_posix()
    scripts_dir_posix = scripts_dir_resolved.as_posix()
    package_name = scripts_dir_resolved.name
    # Package-qualified import keeps intra-package relative imports working,
    # but only exists when the directory name is a legal identifier; with
    # scripts_dir itself on sys.path the direct module import always works.
    if package_name.isidentifier():
        import_stmt = f"from {package_name}.{module_name} import {name}"
    else:
        import_stmt = f"from {module_name} import {name}"
    python_code = f"""
import sys, json
sys.path.insert(0, {scripts_parent!r})
sys.path.insert(0, {scripts_dir_posix!r})
{import_stmt}
params = json.loads(sys.stdin.read())
result = {name}(**params)
print(json.dumps(result))
"""

    # Determine Python executable. Bare "python" is unreliable on Windows
    # (Microsoft Store alias stub), so fall back to this interpreter.
    python_executable = python_path or sys.executable

    return _run_subprocess(python_executable, python_code, params, timeout, log_file, extra_env)


def _run_subprocess(
    python_executable: str,
    python_code: str,
    params: dict,
    timeout: int,
    log_file: Path = None,
    extra_env: dict = None,
) -> dict:
    """Run the experiment child with thread-pumped pipes (portable).

    Two daemon threads drain the child's pipes concurrently: stderr streams
    line-by-line into the log file (live tailing) and stdout accumulates in
    memory. Draining both at once is what prevents the classic deadlock where
    a child blocks writing a large result (e.g. base64 plots > pipe buffer)
    that the parent only reads after exit.

    Timeout behaviour is governed by SCQO_AGENT_TIMEOUT_POLICY:
      - "kill" (default): terminate the whole process tree, raise TimeoutError.
      - "detach": stop waiting but leave the child running and keep draining
        its pipes to EOF, returning a synthesized failed result. This exists
        for hardware backends (QM) where killing a child mid-job orphans the
        instrument-side job and wedges the gateway for every later run.
    """
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    # The child prints its JSON result to stdout; on Windows the default
    # console encoding (cp1252) mangles non-ASCII in it.
    env["PYTHONIOENCODING"] = "utf-8"
    if extra_env:
        env.update({k: str(v) for k, v in extra_env.items()})

    log_fh = None
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_fh = open(log_file, "w", encoding="utf-8")

    stdout_chunks: list[str] = []
    stderr_tail: list[str] = []

    def _pump_stdout(stream):
        while True:
            chunk = stream.read(65536)
            if not chunk:
                break
            stdout_chunks.append(chunk)

    def _pump_stderr(stream):
        for line in stream:
            if log_fh is not None:
                log_fh.write(line)
                log_fh.flush()
            else:
                stderr_tail.append(line)
                del stderr_tail[:-200]

    try:
        process = subprocess.Popen(
            [python_executable, "-c", python_code],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
    except FileNotFoundError:
        if log_fh is not None:
            log_fh.close()
        raise RuntimeError(f"Python interpreter not found: {python_executable}")

    readers = [
        threading.Thread(target=_pump_stdout, args=(process.stdout,), daemon=True),
        threading.Thread(target=_pump_stderr, args=(process.stderr,), daemon=True),
    ]
    for reader in readers:
        reader.start()

    try:
        try:
            process.stdin.write(json.dumps(params))
            process.stdin.close()
        except OSError:
            pass  # child exited before reading stdin; its exit code tells the story

        try:
            returncode = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            policy = os.environ.get("SCQO_AGENT_TIMEOUT_POLICY", "kill").strip().lower()
            if policy == "detach":
                # Reader threads are daemons and keep draining so the child
                # can never block on a full pipe while it finishes its
                # hardware cleanup on its own schedule.
                message = (
                    f"Timed out after {timeout}s. The experiment child process "
                    f"(pid {process.pid}) was left running because "
                    f"SCQO_AGENT_TIMEOUT_POLICY=detach — killing it mid-job can "
                    f"orphan an instrument-side job. Do not retry; notify the "
                    f"operator and wait for the child to finish."
                )
                if log_fh is not None:
                    log_fh.write(f"\n[runner] {message}\n")
                    log_fh.flush()
                return {
                    "status": "failed",
                    "error": message,
                    "results": {"detached_pid": process.pid, "timeout_s": timeout},
                    "arrays": {},
                    "plots": [],
                }
            terminate_tree(process.pid)
            raise TimeoutError(f"Experiment timed out after {timeout} seconds")

        for reader in readers:
            reader.join(timeout=10)

        if returncode != 0:
            if log_fh is not None:
                log_fh.flush()
                error_context = log_file.read_text(encoding="utf-8")[-500:]
            else:
                error_context = "".join(stderr_tail)[-500:] or "Unknown error"
            raise RuntimeError(
                f"Experiment subprocess failed (exit {returncode}): {error_context}"
            )

        return _parse_and_validate_result("".join(stdout_chunks))
    finally:
        if log_fh is not None:
            log_fh.close()


def _parse_and_validate_result(stdout: str) -> dict:
    """Parse JSON output and validate result structure.

    The whole stdout should be exactly one JSON document. If it is not —
    a C-level library wrote to fd 1 past Python's redirect_stdout, or a
    stray print survived — fall back to the last line that parses as a
    JSON object, since the contract puts the result print last.
    """
    try:
        result = json.loads(stdout)
    except json.JSONDecodeError as e:
        result = None
        for line in reversed(stdout.splitlines()):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                candidate = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(candidate, dict):
                result = candidate
                break
        if result is None:
            raise RuntimeError(f"Failed to parse experiment output as JSON: {e}")

    if not isinstance(result, dict):
        raise RuntimeError("Experiment must return a dictionary")

    if "status" not in result:
        raise RuntimeError("Experiment result missing 'status' field")

    if result["status"] not in ("success", "failed"):
        raise RuntimeError(
            f"Invalid status value: {result['status']}. Must be 'success' or 'failed'"
        )

    if result["status"] == "failed" and "error" not in result:
        raise RuntimeError("Failed experiment must include 'error' field")

    _normalise_result_containers(result)
    result["arrays"] = _collect_arrays(result)

    return result


def _normalise_result_containers(result: dict) -> None:
    """Collapse `results` and `data` into one canonical container.

    The documented script return format has no `results` key: a script reports
    its scalars and tagged arrays under `data`. `results` is the name of the
    stored field, and the persistence paths tolerate a script that uses it by
    reading `results` or falling back to `data` — so only one of the two is
    ever consumed downstream.

    That made it possible for the stored scalars and the stored arrays to
    describe different subsets of one run: arrays were gathered from both
    containers while everything else came from whichever container was picked.
    Merging them here means every consumer sees the same single container.
    `results` wins a name collision, matching the precedence the persistence
    paths already apply.
    """
    from_results = result.get("results")
    from_data = result.get("data")
    if not isinstance(from_results, dict) and not isinstance(from_data, dict):
        return

    canonical = {}
    if isinstance(from_data, dict):
        canonical.update(from_data)
    if isinstance(from_results, dict):
        canonical.update(from_results)
    result["results"] = canonical


def _collect_arrays(result: dict) -> dict:
    """Gather every persistable array from a result into one mapping.

    Scripts return arrays nested under `results`/`data` tagged `type:"array"`,
    and may also supply a top-level `arrays` mapping of raw values. Nothing
    else extracts the tagged form, so without this the queryable HDF5 `arrays`
    group would stay empty for those scripts.

    Precedence is the top-level `arrays` mapping, then `results`, then `data`,
    and the first writer of a name wins. Anything already present is therefore
    preserved rather than replaced, while names it does not define are still
    added. Entries that storage could not write are skipped rather than
    raising, since a malformed array should not fail an otherwise good run.
    """
    collected: dict = {}

    # Raw values, already in the shape storage expects.
    existing = result.get("arrays")
    if isinstance(existing, dict):
        for key, value in existing.items():
            if _is_persistable_name(key) and _is_persistable_array(value):
                collected[key] = value

    # Tagged values, which need unwrapping.
    for container_name in ("results", "data"):
        container = result.get(container_name)
        if not isinstance(container, dict):
            continue
        for key, value in container.items():
            if key in collected or not _is_persistable_name(key):
                continue
            if isinstance(value, dict) and value.get("type") == "array":
                candidate = value.get("value")
                if _is_persistable_array(candidate):
                    collected[key] = candidate

    return collected


def _is_persistable_name(name: any) -> bool:
    """Report whether storage could use this name as an HDF5 dataset name.

    Names become dataset names directly. An empty name is not a valid one,
    "." and ".." address the current and parent group rather than a new
    dataset, and a name containing "/" creates intermediate groups, which
    load_experiment then tries to slice as if it were a dataset.
    """
    if not isinstance(name, str) or not name:
        return False
    if "/" in name or "\x00" in name:
        return False
    if name in (".", ".."):
        return False
    # h5py encodes the name as UTF-8. A lone surrogate survives JSON transport
    # but cannot be encoded, so it would raise only at save time.
    try:
        name.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_persistable_array(value: any) -> bool:
    """Report whether storage could write this value and read it back.

    Being a list is not sufficient. core/storage.py builds the dataset with
    np.array() and reads it back by slicing with [:], so a ragged list raises
    from numpy and a list of strings, mappings or None raises from h5py for
    want of a native dtype. Mirroring the real write here keeps a malformed
    array from turning an otherwise successful run into a save failure.
    """
    if not isinstance(value, list):
        return False

    try:
        array = np.asarray(value)
    except (ValueError, TypeError):
        # Ragged nesting cannot become a rectangular array.
        return False

    if not (
        np.issubdtype(array.dtype, np.number)
        or np.issubdtype(array.dtype, np.bool_)
    ):
        return False

    # The dtype alone does not prove the conversion kept the value. Mixing an
    # integer too large for a float mantissa with a float yields a float64
    # array that silently rounds it, so what is read back from storage would
    # differ from what the experiment reported.
    return array.tolist() == value


def _check_type(value: any, type_name: str) -> bool:
    """Check if value matches the expected type (no coercion).

    Args:
        value: Value to check
        type_name: Expected type name (int, float, str, bool, list)

    Returns:
        True if type matches, False otherwise
    """
    type_map = {
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "list": list,
        "dict": dict,
    }

    expected_type = type_map.get(type_name)
    if expected_type is None:
        return False

    # Strict type checking (no coercion)
    # Note: bool is a subclass of int in Python, so check bool before int
    if type_name == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    elif type_name == "float":
        # JSON does not distinguish int from float — accept both
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    else:
        return isinstance(value, expected_type)
