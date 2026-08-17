"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_pair_swap_chevron(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    min_flux_amp_v: float = 0.0,
    max_flux_amp_v: float = 0.3,
    num_amp_points: int = 41,
    min_swap_time_ns: float = 1.0,
    max_swap_time_ns: float = 100.0,
    num_time_points: int = 100,
    drive_side: str = 'low',
    flux_side: str = 'low',
    min_transfer: Annotated[float, (0.0, 1.0)] = 0.3,
) -> dict:
    """Single-excitation swap chevron: excite ONE member of a pair, then sweep a flux pulse (absolute volts) on one member's flux line against its duration, reading both members' joint populations. The arch of the excitation transfer locates the resonance amplitude and the full-swap time — the bring-up step before a coupler decouple point exists. Record-only diagnostic: the per-map summary lands in result.fit and nothing is written back to the device."""
    return run_scqo(
        "pair_swap_chevron",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "min_flux_amp_v": min_flux_amp_v,
            "max_flux_amp_v": max_flux_amp_v,
            "num_amp_points": num_amp_points,
            "min_swap_time_ns": min_swap_time_ns,
            "max_swap_time_ns": max_swap_time_ns,
            "num_time_points": num_time_points,
            "drive_side": drive_side,
            "flux_side": flux_side,
            "min_transfer": min_transfer,
        },
    )
