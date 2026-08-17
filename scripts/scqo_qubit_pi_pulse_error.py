"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_pi_pulse_error(
    targets: list,
    min_amp_factor: float = 0.9,
    max_amp_factor: Annotated[float, (0.0, 2.0)] = 1.1,
    num_amp_points: int = 41,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    gate_counts: list = None,
) -> dict:
    """Sweep pi-pulse amplitude factor across repeated X180 gate sequences (X^1, X^3, X^5...) to amplify and precisely calibrate the pi pulse amplitude."""
    return run_scqo(
        "qubit_pi_pulse_error",
        {
            "targets": targets,
            "min_amp_factor": min_amp_factor,
            "max_amp_factor": max_amp_factor,
            "num_amp_points": num_amp_points,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "gate_counts": gate_counts,
        },
    )
