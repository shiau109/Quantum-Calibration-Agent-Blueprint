"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_t1_bayesian(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_blocks: int = 100,
    num_probes: int = 100,
    adaptive_c: Annotated[float, (0, 1.59)] = 0.51,
    k0: float = 1.0,
    t1_prior_s: float = None,
    t1_min_s: float = 1e-06,
    t1_max_s: float = 0.0001,
    k_min: float = 0.2,
    k_max: float = 100.0,
    interleaved_validation: bool = True,
    min_wait_ns: float = 16,
    max_wait_ns: float = 200000,
    active_reset_per_probe: bool = False,
    ci: Annotated[float, (0, 1)] = 0.9,
) -> dict:
    """Track T1 vs laboratory time with per-shot adaptive Bayesian estimation (Berritta et al., arXiv:2506.09576): each single shot waits tau = c * T1_est from the current posterior and updates it in real time (u = 1/k parametrization), reaching a T1 estimate with a shrinking credible interval in ~num_probes shots per block. Interleaved non-adaptive shots give a classical decay cross-check. Record-only: characterizes T1 stability; qubit_relaxation stays the t1_s authority. REQUIRES a calibrated readou…"""
    return run_scqo(
        "qubit_t1_bayesian",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_blocks": num_blocks,
            "num_probes": num_probes,
            "adaptive_c": adaptive_c,
            "k0": k0,
            "t1_prior_s": t1_prior_s,
            "t1_min_s": t1_min_s,
            "t1_max_s": t1_max_s,
            "k_min": k_min,
            "k_max": k_max,
            "interleaved_validation": interleaved_validation,
            "min_wait_ns": min_wait_ns,
            "max_wait_ns": max_wait_ns,
            "active_reset_per_probe": active_reset_per_probe,
            "ci": ci,
        },
    )
