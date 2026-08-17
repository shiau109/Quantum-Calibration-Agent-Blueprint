"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_t1_ade(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    num_blocks: int = 100,
    t0_ns: float = 16,
    t1_guess_s: float = 5e-05,
    dt_factor: float = 1.0,
    adaptive_dt: bool = False,
    min_dt_ns: float = 16,
    max_dt_ns: float = 200000,
    n_bootstrap: int = 300,
) -> dict:
    """Track T1 vs laboratory time: each block measures P(|1>) at three interleaved delays t0/t0+dt/t0+3dt and the instrument computes the closed-form decay rate + analytic sigma in real time (ADE, arXiv:2602.11912 — SPAM cancels, no confusion matrix). Streams a T1 trace with per-point error bars plus the raw shots for a host bootstrap cross-check. Record-only: characterizes T1 stability (drift, spread); qubit_relaxation stays the t1_s authority. reset_method='active' recommended (the shot rate IS the…"""
    return run_scqo(
        "qubit_t1_ade",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "num_blocks": num_blocks,
            "t0_ns": t0_ns,
            "t1_guess_s": t1_guess_s,
            "dt_factor": dt_factor,
            "adaptive_dt": adaptive_dt,
            "min_dt_ns": min_dt_ns,
            "max_dt_ns": max_dt_ns,
            "n_bootstrap": n_bootstrap,
        },
    )
