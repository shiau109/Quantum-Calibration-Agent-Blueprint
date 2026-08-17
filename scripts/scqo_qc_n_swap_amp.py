"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qc_n_swap_amp(
    targets: list,
    readout_mode: str = 'average',
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    min_flux_amp_v: float = 0.0,
    max_flux_amp_v: float = 0.1,
    num_amp_points: int = 21,
    swap_counts: list = None,
    swap_operation: str = 'iswap',
    operation_gap_ns: int = 0,
    drive_side: str = 'low',
    flux_side: str = 'low',
    min_transfer: Annotated[float, (0.0, 1.0)] = 0.3,
) -> dict:
    """N-swap swap-amplitude error-amplification map: excite ONE member of a pair, then apply N repeated swaps (each at the same swept control-qubit flux amplitude, absolute volts) and read both members' joint populations. Repeating the swap amplifies a small swap-amplitude miscalibration, so the populations vs (flux amplitude, N) locate the correctly calibrated amplitude far more finely than a single swap. readout_mode='shot' keeps every shot (per-member states) instead of the averaged joint distribu…"""
    return run_scqo(
        "qc_n_swap_amp",
        {
            "targets": targets,
            "readout_mode": readout_mode,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "min_flux_amp_v": min_flux_amp_v,
            "max_flux_amp_v": max_flux_amp_v,
            "num_amp_points": num_amp_points,
            "swap_counts": swap_counts,
            "swap_operation": swap_operation,
            "operation_gap_ns": operation_gap_ns,
            "drive_side": drive_side,
            "flux_side": flux_side,
            "min_transfer": min_transfer,
        },
    )
