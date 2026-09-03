"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qc_unidirectional_trotter(
    targets: list,
    first_pair: str = None,
    second_pair: str = None,
    reset_qubit: str = None,
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
) -> dict:
    """Unidirectional (cascaded) coupling by Trotterization on a three-qubit chain: excite the chain source once, then repeat N times a partial swap source->relay, a partial swap relay->sink, a parametric reset of the relay and a per-qubit off-resonant AC-Stark phase compensation, reading every chain qubit out at the end. Dumping the relay each round destroys the sink's return path, so the coupling is one-way and the populations vs N show the excitation walking from source to sink while the relay stay…"""
    return run_scqo(
        "qc_unidirectional_trotter",
        {
            "targets": targets,
            "first_pair": first_pair,
            "second_pair": second_pair,
            "reset_qubit": reset_qubit,
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
        },
    )
