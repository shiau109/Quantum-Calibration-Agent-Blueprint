"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_resonator_spectroscopy(
    targets: list,
    start_readout_detuning_hz: float = -10000000.0,
    end_readout_detuning_hz: float = 10000000.0,
    num_readout_freq_points: int = 101,
    num_averages: int = 100,
    readout_amplitude: float = None,
    depletion_factor: float = 10.0,
    analysis_method: str = 'lorentzian',
    baseline_order: Annotated[int, (0, 2)] = 1,
) -> dict:
    """Sweep readout frequency around each resonator and locate the transmission dip; updates each target's readout channel readout_freq_hz and proposes the dip position (f_dress0_hz) and linewidth (kappa_tot_hz) on the attached resonator mode, plus depletion_factor / (2 pi x kappa_tot_hz) as the readout channel's readout_depletion_s knob — this is the experiment that calibrates the photon-depletion wait every other experiment leaves after a readout."""
    return run_scqo(
        "resonator_spectroscopy",
        {
            "targets": targets,
            "start_readout_detuning_hz": start_readout_detuning_hz,
            "end_readout_detuning_hz": end_readout_detuning_hz,
            "num_readout_freq_points": num_readout_freq_points,
            "num_averages": num_averages,
            "readout_amplitude": readout_amplitude,
            "depletion_factor": depletion_factor,
            "analysis_method": analysis_method,
            "baseline_order": baseline_order,
        },
    )
