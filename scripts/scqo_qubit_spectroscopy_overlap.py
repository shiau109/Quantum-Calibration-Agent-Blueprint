"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_spectroscopy_overlap(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    frequency_span_hz: float = 60000000.0,
    num_points: int = 201,
    drive_power_dbm: float = -25.0,
    drive_len_ns: float = None,
    acq_start_ns: float = 0.0,
) -> dict:
    """Two-tone spectroscopy with the saturation drive and the readout tone started TOGETHER, the ADC opening only after both have been on for acq_start_ns so it integrates a steady state. Recalibrates the drive channel's drive_freq_hz from the strongest peak like qubit_spectroscopy, and is faster (no drive-then-readout dead time) — but the live readout tone AC-Stark shifts the qubit, so the frequency it writes back carries that shift unless readout_amp is kept low. Use qubit_spectroscopy for the bare…"""
    return run_scqo(
        "qubit_spectroscopy_overlap",
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
            "acq_start_ns": acq_start_ns,
        },
    )
