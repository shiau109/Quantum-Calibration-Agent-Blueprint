"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from _scqo_runtime import run_scqo


def scqo_qubit_spectroscopy_flux_pulse(
    targets: list,
    flux_component: str = None,
    start_drive_detuning_hz: float = -200000000.0,
    end_drive_detuning_hz: float = 200000000.0,
    num_drive_freq_points: int = 101,
    min_flux_v: float = -0.3,
    max_flux_v: float = 0.3,
    num_flux_points: int = 21,
    num_averages: int = 100,
    ec_ghz: float = 0.2,
    drive_power_dbm: float = -25.0,
) -> dict:
    """2D qubit spectroscopy vs PULSED flux (bias applied only during the drive; readout at idle flux every slice, reduced against one global IQ reference): finds the 0-1 peak at every flux and fits the transmon arch. The flux window is RELATIVE to the channel's idle_flux (0 = stay parked), so a well-tuned qubit maps an arch centred on 0. Proposes sweet spot (flux_offset, absolute), flux period (flux_per_phi0) on the target's flux channel and ej_sum_hz/f_q_max_hz on the target mode as physical facts (…"""
    return run_scqo(
        "qubit_spectroscopy_flux_pulse",
        {
            "targets": targets,
            "flux_component": flux_component,
            "start_drive_detuning_hz": start_drive_detuning_hz,
            "end_drive_detuning_hz": end_drive_detuning_hz,
            "num_drive_freq_points": num_drive_freq_points,
            "min_flux_v": min_flux_v,
            "max_flux_v": max_flux_v,
            "num_flux_points": num_flux_points,
            "num_averages": num_averages,
            "ec_ghz": ec_ghz,
            "drive_power_dbm": drive_power_dbm,
        },
    )
