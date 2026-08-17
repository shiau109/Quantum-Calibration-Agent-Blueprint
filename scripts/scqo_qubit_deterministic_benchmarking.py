"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_deterministic_benchmarking(
    targets: list,
    min_amp_factor: float = 0.9,
    max_amp_factor: Annotated[float, (0.0, 2.0)] = 1.1,
    num_amp_points: int = 1,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    target_gate: str = 'x180',
    max_repetitions: int = 100,
    step: int = None,
    repetitions: list = None,
    amp_prefactors: list = None,
) -> dict:
    """Amplitude error amplification: plays ONE target gate N times and sweeps N, so a small per-gate over/under-rotation accumulates into a resolvable fringe. Repeated across an amplitude-scale sweep, the fringe rate crosses zero at the correct amplitude. Calibrates whichever gate is benchmarked — pi (x180/y180) proposes pi_amp, pi/2 (x90/y90/-x90/-y90) proposes pi_amp_x90 — so it is how the pi/2 gets calibrated in its own right rather than assumed to be half the pi. Far more sensitive than power Rab…"""
    return run_scqo(
        "qubit_deterministic_benchmarking",
        {
            "targets": targets,
            "min_amp_factor": min_amp_factor,
            "max_amp_factor": max_amp_factor,
            "num_amp_points": num_amp_points,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "target_gate": target_gate,
            "max_repetitions": max_repetitions,
            "step": step,
            "repetitions": repetitions,
            "amp_prefactors": amp_prefactors,
        },
    )
