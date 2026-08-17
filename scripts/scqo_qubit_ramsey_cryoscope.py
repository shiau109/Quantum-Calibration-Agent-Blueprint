"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_ramsey_cryoscope(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 2000,
    flux_pulse_amp_v: float = 0.1,
    max_duration_ns: Annotated[int, (32, 2000)] = 240,
    num_frames: int = 16,
    fit_start_fractions: list = None,
    fit_tau_seeds: list = None,
) -> dict:
    """Reconstruct the flux line's step response with a Ramsey phase-tomography sequence — a flux pulse of swept DURATION (1 ns resolution) between two x90 pulses, the second's FRAME swept through a turn — and fit it to a sum of exponentials. Proposes the flux channel's paired distortion facts (distortion_amp, relative; distortion_tau_s, seconds) that describe the cryo-wiring transient; applying them to the instrument's output filter is a manual vendor step. The flux-pulse amplitude is a volts paramet…"""
    return run_scqo(
        "qubit_ramsey_cryoscope",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "flux_pulse_amp_v": flux_pulse_amp_v,
            "max_duration_ns": max_duration_ns,
            "num_frames": num_frames,
            "fit_start_fractions": fit_start_fractions,
            "fit_tau_seeds": fit_tau_seeds,
        },
    )
