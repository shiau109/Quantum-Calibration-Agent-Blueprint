"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_spectroscopy(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    start_drive_detuning_hz: float = -30000000.0,
    end_drive_detuning_hz: float = 30000000.0,
    num_drive_freq_points: int = 201,
    num_averages: int = 100,
    drive_power_dbm: float = -25.0,
    drive_len_ns: float = 20000.0,
    readout_overlap: bool = False,
    acq_start_ns: float = 0.0,
) -> dict:
    """Sweep a weak saturation drive around drive_freq_hz and fit the response peaks; the strongest peak recalibrates the drive channel's drive_freq_hz (coarse two-tone — run after resonator spectroscopy and before power Rabi / Ramsey). readout_overlap=false (the default) ends the drive before the readout tone, which is the bare f_01. readout_overlap=true instead ends it WITH the tone, so the ADC integrates a steady state under a live drive — faster (no drive-then-readout dead time) and it shows the l…"""
    return run_scqo(
        "qubit_spectroscopy",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "start_drive_detuning_hz": start_drive_detuning_hz,
            "end_drive_detuning_hz": end_drive_detuning_hz,
            "num_drive_freq_points": num_drive_freq_points,
            "num_averages": num_averages,
            "drive_power_dbm": drive_power_dbm,
            "drive_len_ns": drive_len_ns,
            "readout_overlap": readout_overlap,
            "acq_start_ns": acq_start_ns,
        },
    )
