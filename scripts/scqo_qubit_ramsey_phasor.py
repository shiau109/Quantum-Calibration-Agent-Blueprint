"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_ramsey_phasor(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    min_idle_time_ns: float = 16,
    max_idle_time_ns: float = 200000,
    num_points: int = 60,
    num_frames: int = 16,
    fix_p: float = None,
) -> dict:
    """Two pi/2 pulses separated by a LOG-spaced idle time, with the closing pulse's phase swept through a full turn at every idle point. A lock-in over that frame axis reads the coherence envelope off the phasor magnitude and the accumulated phase off its angle, so T2* comes straight from the envelope instead of being fitted out of a decaying oscillation. Reports the stretch exponent p of the decay (1 = Markovian/white noise, 2 = the Gaussian decay of a 1/f-dominated environment) alongside T2*, which…"""
    return run_scqo(
        "qubit_ramsey_phasor",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "min_idle_time_ns": min_idle_time_ns,
            "max_idle_time_ns": max_idle_time_ns,
            "num_points": num_points,
            "num_frames": num_frames,
            "fix_p": fix_p,
        },
    )
