"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_thermal_population(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_shots: int = 10000,
) -> dict:
    """Prepare |g> only and record every readout shot's I/Q point, then split the cloud against the readout channel's STORED |g>/|e> blob centers to get the residual excited-state population at idle — the chip's thermal population, written back as the mode fact n_th. Reported twice: pop_e_prep_g is the fitted mixture weight (readout overlap removed, the value stored) and p_e_given_g is the counted fraction (population + overlap error, run-record-only); their difference is the discrimination error. REQ…"""
    return run_scqo(
        "qubit_thermal_population",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_shots": num_shots,
        },
    )
