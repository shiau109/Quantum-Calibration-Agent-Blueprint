"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_spectroscopy_cryoscope(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    flux_pulse_amp_v: float = 0.1,
    min_detuning_hz: float = -100000000.0,
    max_detuning_hz: float = 100000000.0,
    num_freq_points: int = 101,
    drive_len_ns: float = 400.0,
    min_wait_ns: int = 16,
    max_wait_ns: int = 20000,
    num_wait_points: int = 50,
    ec_ghz: float = 0.2,
    fallback_curvature_hz_per_v2: float = -1000000000.0,
    fit_start_fractions: list = None,
    fit_tau_seeds: list = None,
) -> dict:
    """Reconstruct the flux line's LONG-TIME (microsecond) step response by qubit spectroscopy vs wait-time into a parked flux pulse, and fit it to a sum of exponentials. The complement of qubit_ramsey_cryoscope: spectroscopy reads the frequency directly, so it reaches the slow bias-tee/wiring tails a phase measurement cannot. Proposes the flux channel's paired distortion facts (distortion_amp, relative; distortion_tau_s, seconds) — the same facts the Ramsey cryoscope writes, as an INDEPENDENT full me…"""
    return run_scqo(
        "qubit_spectroscopy_cryoscope",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "flux_pulse_amp_v": flux_pulse_amp_v,
            "min_detuning_hz": min_detuning_hz,
            "max_detuning_hz": max_detuning_hz,
            "num_freq_points": num_freq_points,
            "drive_len_ns": drive_len_ns,
            "min_wait_ns": min_wait_ns,
            "max_wait_ns": max_wait_ns,
            "num_wait_points": num_wait_points,
            "ec_ghz": ec_ghz,
            "fallback_curvature_hz_per_v2": fallback_curvature_hz_per_v2,
            "fit_start_fractions": fit_start_fractions,
            "fit_tau_seeds": fit_tau_seeds,
        },
    )
