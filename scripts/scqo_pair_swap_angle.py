"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_pair_swap_angle(
    targets: list,
    readout_mode: str = 'average',
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    min_coupler_flux_v: float = 0.0,
    max_coupler_flux_v: float = 0.1,
    num_coupler_points: int = 21,
    swap_counts: list = None,
    swap_operation: str = 'partial_swap',
    target_theta_rad: float = None,
    compensation_amps: dict = None,
    stark_operation: str = 'stark',
    stark_detuning_hz: float = 50000000.0,
    operation_gap_ns: int = 0,
    drive_side: str = 'low',
    flux_side: str = 'low',
    min_transfer: Annotated[float, (0.0, 1.0)] = 0.3,
) -> dict:
    """Partial-swap ANGLE calibration: excite ONE member of a pair, apply N repeated swaps at the same swept COUPLER flux amplitude (the angle knob — the member's own flux stays at its calibrated resonance value), and read both members' joint populations. At each coupler amplitude the transfer oscillates in N with period pi/theta, so a cosine fit per coupler row yields the calibration curve theta(coupler flux) and, given target_theta_rad, the amplitude that delivers a wanted angle. What is fitted is t…"""
    return run_scqo(
        "pair_swap_angle",
        {
            "targets": targets,
            "readout_mode": readout_mode,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "min_coupler_flux_v": min_coupler_flux_v,
            "max_coupler_flux_v": max_coupler_flux_v,
            "num_coupler_points": num_coupler_points,
            "swap_counts": swap_counts,
            "swap_operation": swap_operation,
            "target_theta_rad": target_theta_rad,
            "compensation_amps": compensation_amps,
            "stark_operation": stark_operation,
            "stark_detuning_hz": stark_detuning_hz,
            "operation_gap_ns": operation_gap_ns,
            "drive_side": drive_side,
            "flux_side": flux_side,
            "min_transfer": min_transfer,
        },
    )
