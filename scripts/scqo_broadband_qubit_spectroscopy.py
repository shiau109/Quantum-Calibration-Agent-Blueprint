"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_broadband_qubit_spectroscopy(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    start_freq_hz: float = 3000000000.0,
    stop_freq_hz: float = 6500000000.0,
    bandwidth_per_lo_hz: float = 300000000.0,
    num_points_per_lo: int = 201,
    lo_gap_hz: float = 10000000.0,
    drive_power_dbm: float = -25.0,
    drive_len_ns: float = 20000.0,
    max_peaks: int = 1,
    prominence: float = 0.1,
    min_snr: float = 6.0,
) -> dict:
    """Sweep qubit XY drive frequency across a wideband range by stepping drive LO sub-bands, detect candidate qubit transition peaks, and mark candidate frequencies without updating device state."""
    return run_scqo(
        "broadband_qubit_spectroscopy",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "start_freq_hz": start_freq_hz,
            "stop_freq_hz": stop_freq_hz,
            "bandwidth_per_lo_hz": bandwidth_per_lo_hz,
            "num_points_per_lo": num_points_per_lo,
            "lo_gap_hz": lo_gap_hz,
            "drive_power_dbm": drive_power_dbm,
            "drive_len_ns": drive_len_ns,
            "max_peaks": max_peaks,
            "prominence": prominence,
            "min_snr": min_snr,
        },
    )
