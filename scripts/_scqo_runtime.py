"""SCQO session adapter for QCA experiment wrappers.

Runs inside the experiment subprocess, under the SCQO backend venv named by
SCQO_AGENT_PYTHON (see tools/lab_tool.py). Public wrapper scripts call
run_scqo(); everything QCA-specific about how an SCQO run is opened,
executed, and mapped into QCA's result contract lives here.

Environment contract (set by launch/run-*.ps1):
  SCQO_AGENT_CONFIG   path to the deployment's lab config.toml (required)
  SCQO_USER_CONFIG    path to the deployment's user-overlay toml, or "none"
                      (required to be SET — if it were unset, SCQO would
                      fall back to the operator's personal ~/.scqo/user.toml,
                      which on this machine can steer runs to real hardware)
  QCA_EXP_ID          QCA-side experiment id, stamped into the run note

Writeback policy: update="suggest" is hardcoded. The agent proposes
parameter changes; a human accepts them with the SCQO CLI. Wrappers do not
expose an update parameter, so the agent cannot request "apply".
"""

from __future__ import annotations

import base64
import contextlib
import json
import os
import re
import sys
from pathlib import Path

# Set before any scqo/matplotlib import: without a pinned headless backend a
# GUI matplotlib can fail mid-run on Windows and the figure PNGs are lost.
os.environ.setdefault("MPLBACKEND", "Agg")

MAX_ARRAYS = 16
MAX_ARRAY_POINTS = 65536

_SESSION = None
_CONFIG = None


def _fail(message: str) -> dict:
    return {"status": "failed", "error": message, "results": {}, "arrays": {}, "plots": []}


def _session():
    """Build (once) and return the (Session, LabConfig) pair for this process."""
    global _SESSION, _CONFIG
    if _SESSION is not None:
        return _SESSION, _CONFIG

    config_path = os.environ.get("SCQO_AGENT_CONFIG", "").strip()
    if not config_path:
        raise RuntimeError(
            "SCQO_AGENT_CONFIG is not set. Start the server via "
            "launch/run-sim.ps1, run-qblox.ps1, or run-qm.ps1, which pin the "
            "deployment's lab config."
        )
    if not Path(config_path).is_file():
        raise RuntimeError(f"SCQO_AGENT_CONFIG points to a missing file: {config_path}")

    user_config = os.environ.get("SCQO_USER_CONFIG", "").strip()
    if not user_config:
        raise RuntimeError(
            "SCQO_USER_CONFIG is not set. It must name the deployment's "
            "user-overlay toml (or the literal string 'none'); when unset, "
            "SCQO falls back to the operator's personal ~/.scqo/user.toml, "
            "which can silently select a different device or a real "
            "instrument. Use the launch scripts."
        )

    from scqo.cli import build_session

    sess, cfg = build_session(config_path)

    # The classic leak: no parameters_file pinned anywhere -> SCQO silently
    # applies ~/.scqo/parameters.toml, whose standing defaults can change
    # what the agent's runs measure. Refuse to run in that state.
    personal_params = Path.home() / ".scqo" / "parameters.toml"
    source = cfg.parameters_source
    if source is not None and Path(source).resolve() == personal_params.resolve():
        raise RuntimeError(
            "This deployment resolved its parameter defaults from the "
            f"personal {personal_params} — pin parameters_file in the "
            "deployment config/user overlay instead (configs/*.toml)."
        )

    _SESSION, _CONFIG = sess, cfg
    return _SESSION, _CONFIG


def _setup_stamp(sess, cfg) -> dict:
    return {
        "device": cfg.device,
        "setup": getattr(sess, "setup_name", ""),
        "backend": getattr(sess, "backend_label", ""),
        "cooldown": getattr(sess, "cooldown_id", ""),
        "config": str(cfg.source) if cfg.source else None,
    }


def _sanitize_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name) or "unnamed"


def _collect_plots(figures: list[str]) -> list[dict]:
    """Base64-encode figure PNGs as QCA plot entries with unique names."""
    plots = []
    seen = set()
    for fig_path in figures:
        path = Path(fig_path)
        try:
            data = base64.b64encode(path.read_bytes()).decode("ascii")
        except OSError:
            continue
        # analysis/<target>/<estimator>.png -> "<target>__<estimator>"
        name = _sanitize_name(f"{path.parent.name}__{path.stem}")
        candidate, n = name, 1
        while candidate in seen:
            n += 1
            candidate = f"{name}_{n}"
        seen.add(candidate)
        plots.append({"name": candidate, "format": "png", "data": data})
    return plots


def _collect_arrays(sess, run_id: str) -> dict:
    """Best-effort 1-D numeric slices of the run dataset for QCA's array tools."""
    import numpy as np

    arrays: dict = {}
    try:
        ds = sess.datastore.open_dataset(run_id)
    except Exception:
        return arrays

    def _add(name, values):
        if len(arrays) >= MAX_ARRAYS:
            return
        arr = np.asarray(values)
        if arr.ndim != 1 or arr.size == 0 or arr.size > MAX_ARRAY_POINTS:
            return
        if not np.issubdtype(arr.dtype, np.number) or np.iscomplexobj(arr):
            return
        if not np.all(np.isfinite(arr)):
            return  # NaN/inf don't survive the JSON->HDF5 path
        arrays[_sanitize_name(name)] = arr.tolist()

    try:
        for coord_name in ds.coords:
            _add(f"coord__{coord_name}", ds.coords[coord_name].values)
        for var_name in ds.data_vars:
            var = ds[var_name]
            if "target" in var.dims:
                for target in ds.coords.get("target", []).values:
                    _add(f"{target}__{var_name}", var.sel(target=target).values)
            else:
                _add(str(var_name), var.values)
    except Exception:
        pass
    finally:
        with contextlib.suppress(Exception):
            ds.close()
    return arrays


def run_scqo(experiment: str, params: dict) -> dict:
    """Run one SCQO experiment and map its outcome to QCA's result contract.

    Never raises: every failure comes back as {"status": "failed", ...} so a
    plumbing problem and a physics verdict travel the same, parseable road.
    """
    try:
        # Omitted-optional convention: wrapper signatures use None defaults
        # for SCQO's optional parameters; only explicitly-set values are sent
        # so SCQO applies its own real defaults.
        params = {k: v for k, v in params.items() if v is not None}

        sess, cfg = _session()

        note = ""
        qca_exp_id = os.environ.get("QCA_EXP_ID", "").strip()
        if qca_exp_id:
            note = f"qca:{qca_exp_id}"

        # Vendor code prints progress bars to stdout (QM's progress_counter,
        # some Qblox update() paths); stdout must stay clean for the final
        # JSON, so everything inside the run is redirected to stderr.
        with contextlib.redirect_stdout(sys.stderr):
            payload = sess.run(
                experiment,
                params,
                update="suggest",
                tags=["qca"],
                note=note,
            )

            run_id = payload.get("run_id")
            loaded = {}
            if run_id:
                with contextlib.suppress(Exception):
                    loaded = sess.load_run(run_id)

            arrays = _collect_arrays(sess, run_id) if run_id else {}

        outcomes = payload.get("outcomes", {}) or {}
        record_outcome = (loaded.get("record") or {}).get("outcome")
        scqo_error = payload.get("error")

        results = {
            "run_id": run_id,
            "data_path": payload.get("data_path"),
            "setup": _setup_stamp(sess, cfg),
            "outcomes": outcomes,
            "record_outcome": record_outcome,
            "fit": payload.get("fit", {}),
            "suggestions": payload.get("suggestions", []),
            "update_mode": "suggest",
        }
        if scqo_error:
            results["scqo_error"] = scqo_error
        if payload.get("datastore_error"):
            results["datastore_error"] = payload["datastore_error"]

        plots = _collect_plots(loaded.get("figures", []))

        if scqo_error:
            status, error = "failed", str(scqo_error)
        elif any(v == "successful" for v in outcomes.values()):
            status, error = "success", None
        else:
            status = "failed"
            verdicts = ", ".join(f"{t}: {v}" for t, v in outcomes.items()) or "no outcomes"
            error = f"No target succeeded ({verdicts})."

        result = {"status": status, "results": results, "arrays": arrays, "plots": plots}
        if error:
            result["error"] = error
        return result

    except Exception as exc:  # noqa: BLE001 — the contract is a failed dict, never a traceback
        return _fail(f"{type(exc).__name__}: {exc}")
