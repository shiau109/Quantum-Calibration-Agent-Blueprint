"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qc_trotter_compensation(
    targets: list,
    first_pair: str = None,
    second_pair: str = None,
    reset_qubit: str = None,
    compensation_target: str = None,
    readout_mode: str = 'average',
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    compensation_amps: dict = None,
    max_rounds: int = 20,
    swap_operation: str = 'partial_swap',
    reset_operation: str = 'reset',
    swap_coupler_flux: dict = None,
    stark_operation: str = 'stark',
    stark_detuning_hz: float = 50000000.0,
    prep_qubit: str = None,
    prep_operation: str = 'x180',
    operation_gap_ns: int = 0,
    min_transfer: Annotated[float, (0.0, 1.0)] = 0.05,
    min_compensation_amp: float = 0.0,
    max_compensation_amp: float = 1.0,
    num_amp_points: int = 21,
) -> dict:
    """Trotter-chain AC-Stark compensation scan: run the unidirectional-coupling chain over a 2-D sweep of ONE qubit's Stark compensation amplitude against the Trotter-step count, and report the amplitude that maximises transport to the sink. Only the differential source-sink phase is observable, so one amplitude is swept and the reset qubit is refused as the target. Sweeping N too is what makes the answer trustworthy: cancelling rounds leave the sink peaking at N=1 while adding rounds push the peak o…"""
    return run_scqo(
        "qc_trotter_compensation",
        {
            "targets": targets,
            "first_pair": first_pair,
            "second_pair": second_pair,
            "reset_qubit": reset_qubit,
            "compensation_target": compensation_target,
            "readout_mode": readout_mode,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "compensation_amps": compensation_amps,
            "max_rounds": max_rounds,
            "swap_operation": swap_operation,
            "reset_operation": reset_operation,
            "swap_coupler_flux": swap_coupler_flux,
            "stark_operation": stark_operation,
            "stark_detuning_hz": stark_detuning_hz,
            "prep_qubit": prep_qubit,
            "prep_operation": prep_operation,
            "operation_gap_ns": operation_gap_ns,
            "min_transfer": min_transfer,
            "min_compensation_amp": min_compensation_amp,
            "max_compensation_amp": max_compensation_amp,
            "num_amp_points": num_amp_points,
        },
    )
