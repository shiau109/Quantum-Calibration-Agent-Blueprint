"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_drag_alternating(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    min_beta: float = -2.0,
    max_beta: float = 2.0,
    num_beta_points: int = 41,
    max_pulses: int = 20,
    num_pulse_points: int = 10,
    target_gate: str = 'x180',
) -> dict:
    """Sweep DRAG beta coefficient and play alternating pulse sequences. The DRAG value that minimizes error accumulation (stays flat at ground state) is the optimal calibration point."""
    return run_scqo(
        "qubit_drag_alternating",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "min_beta": min_beta,
            "max_beta": max_beta,
            "num_beta_points": num_beta_points,
            "max_pulses": max_pulses,
            "num_pulse_points": num_pulse_points,
            "target_gate": target_gate,
        },
    )
