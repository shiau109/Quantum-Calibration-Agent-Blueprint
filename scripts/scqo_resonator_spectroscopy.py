"""GENERATED-STYLE WRAPPER — keep in sync with codegen/generate_wrappers.py output."""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_resonator_spectroscopy(
    targets: list,
    num_averages: int = 100,
    frequency_span_hz: float = 20000000.0,
    num_points: int = 101,
    readout_amplitude: float = None,
    depletion_factor: float = 10.0,
    analysis_method: str = "lorentzian",
    baseline_order: Annotated[int, (0, 2)] = 1,
) -> dict:
    """Sweep readout frequency around each resonator and locate the transmission dip; updates each target's readout channel readout_freq_hz and proposes the dip position (f_r_hz) and linewidth (kappa_tot_hz). analysis_method: 'lorentzian' or 'circle' (use 'lorentzian' on the simulated backend)."""
    return run_scqo(
        "resonator_spectroscopy",
        {
            "targets": targets,
            "num_averages": num_averages,
            "frequency_span_hz": frequency_span_hz,
            "num_points": num_points,
            "readout_amplitude": readout_amplitude,
            "depletion_factor": depletion_factor,
            "analysis_method": analysis_method,
            "baseline_order": baseline_order,
        },
    )
