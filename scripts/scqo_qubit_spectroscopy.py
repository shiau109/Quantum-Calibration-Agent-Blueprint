"""GENERATED-STYLE WRAPPER — keep in sync with codegen/generate_wrappers.py output."""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_spectroscopy(
    targets: list,
    reset_method: str = "thermal",
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    frequency_span_hz: float = 60000000.0,
    num_points: int = 201,
    drive_power_dbm: float = -25.0,
    drive_len_ns: float = None,
) -> dict:
    """Sweep a weak saturation drive around drive_freq_hz and fit the response peaks; the strongest peak recalibrates the drive channel's drive_freq_hz (coarse two-tone — run after resonator spectroscopy). reset_method: 'thermal' or 'active' (active requires an accepted single_shot_readout)."""
    return run_scqo(
        "qubit_spectroscopy",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "frequency_span_hz": frequency_span_hz,
            "num_points": num_points,
            "drive_power_dbm": drive_power_dbm,
            "drive_len_ns": drive_len_ns,
        },
    )
