"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_pair_swap_flux_map(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    min_coupler_flux_v: float = -0.15,
    max_coupler_flux_v: float = 0.15,
    num_coupler_points: int = 31,
    min_qubit_flux_v: float = 0.0,
    max_qubit_flux_v: float = 0.2,
    num_qubit_points: int = 21,
    swap_time_ns: float = None,
    flux_pulse_shape: str = 'square',
    drive_side: str = 'low',
    flux_side: str = 'low',
    min_transfer: Annotated[float, (0.0, 1.0)] = 0.3,
) -> dict:
    """Fixed-duration 2D swap map: excite ONE member of a pair, then play a coupler flux pulse and a member flux pulse simultaneously over a fixed window, sweeping both amplitudes (absolute volts) and reading both members' joint populations. The excitation-transfer spot shows where the pair swaps and how the coupler bias moves that point — the fixed-time sibling of pair_swap_chevron. Record-only diagnostic: the per-map summary lands in result.fit and nothing is written back."""
    return run_scqo(
        "pair_swap_flux_map",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "min_coupler_flux_v": min_coupler_flux_v,
            "max_coupler_flux_v": max_coupler_flux_v,
            "num_coupler_points": num_coupler_points,
            "min_qubit_flux_v": min_qubit_flux_v,
            "max_qubit_flux_v": max_qubit_flux_v,
            "num_qubit_points": num_qubit_points,
            "swap_time_ns": swap_time_ns,
            "flux_pulse_shape": flux_pulse_shape,
            "drive_side": drive_side,
            "flux_side": flux_side,
            "min_transfer": min_transfer,
        },
    )
