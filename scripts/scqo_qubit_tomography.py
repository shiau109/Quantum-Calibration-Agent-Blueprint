"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_tomography(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    qubit_configs: dict = None,
    gate_counts: list = None,
    interleave_noise: bool = True,
    symmetrized_readout: bool = True,
    num_training_shots: int = 2000,
) -> dict:
    """Performs state tomography by applying init states, target gates, and sweeping basis rotations to measure populations and gate error trajectory."""
    return run_scqo(
        "qubit_tomography",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "qubit_configs": qubit_configs,
            "gate_counts": gate_counts,
            "interleave_noise": interleave_noise,
            "symmetrized_readout": symmetrized_readout,
            "num_training_shots": num_training_shots,
        },
    )
