"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_drag_equator(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    min_beta: float = -0.5,
    max_beta: float = 0.5,
    num_beta_points: int = 41,
    pulse_repetitions: int = 3,
    target_gate: str = 'x180',
) -> dict:
    """Sweep the DRAG beta coefficient and play three sequences (Seq 0: X90-(Y180)^N, Seq 1: X90-(-Y180)^N, Seq 2: X90-(X180)^N). The intersection of the three lines determines the optimal DRAG beta."""
    return run_scqo(
        "qubit_drag_equator",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "min_beta": min_beta,
            "max_beta": max_beta,
            "num_beta_points": num_beta_points,
            "pulse_repetitions": pulse_repetitions,
            "target_gate": target_gate,
        },
    )
