"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from _scqo_runtime import run_scqo


def scqo_broadband_resonator_spectroscopy(
    targets: list,
    num_averages: int = 100,
    start_freq_hz: float = 4000000000.0,
    stop_freq_hz: float = 8000000000.0,
    bandwidth_per_lo_hz: float = 400000000.0,
    num_points_per_lo: int = 201,
    lo_gap_hz: float = 10000000.0,
    num_dips: int = None,
    readout_amplitude: float = None,
    readout_power_dbm: float = None,
    min_prominence_db: float = 0.5,
    min_snr: float = 2.5,
) -> dict:
    """Sweep readout frequency across a wideband range by stepping LO sub-bands, detect transmission dips, and mark the candidate resonator frequencies determined from components.toml without updating device state."""
    return run_scqo(
        "broadband_resonator_spectroscopy",
        {
            "targets": targets,
            "num_averages": num_averages,
            "start_freq_hz": start_freq_hz,
            "stop_freq_hz": stop_freq_hz,
            "bandwidth_per_lo_hz": bandwidth_per_lo_hz,
            "num_points_per_lo": num_points_per_lo,
            "lo_gap_hz": lo_gap_hz,
            "num_dips": num_dips,
            "readout_amplitude": readout_amplitude,
            "readout_power_dbm": readout_power_dbm,
            "min_prominence_db": min_prominence_db,
            "min_snr": min_snr,
        },
    )
