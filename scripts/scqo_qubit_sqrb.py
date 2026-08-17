"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_sqrb(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    num_random_sequences: int = 30,
    max_circuit_depth: int = 200,
    delta_clifford: int = 20,
    log_scale: bool = True,
    seed: int = None,
) -> dict:
    """Single Qubit Randomized Benchmarking (SQRB) to measure average gate fidelity."""
    return run_scqo(
        "qubit_sqrb",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "num_random_sequences": num_random_sequences,
            "max_circuit_depth": max_circuit_depth,
            "delta_clifford": delta_clifford,
            "log_scale": log_scale,
            "seed": seed,
        },
    )
