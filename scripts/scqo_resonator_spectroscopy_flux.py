"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_resonator_spectroscopy_flux(
    targets: list,
    flux_component: str = None,
    min_flux_v: float = -0.3,
    max_flux_v: float = 0.3,
    num_flux_points: int = 21,
    num_averages: int = 100,
    frequency_span_hz: float = 20000000.0,
    num_freq_points: int = 101,
    f_q_max_hz: float = None,
    analysis_method: str = 'dispersive',
    edge_margin_frac: Annotated[float, (0, 0.5)] = 0.06,
    dip_method: str = 'lorentzian',
) -> dict:
    """2D resonator spectroscopy vs ABSOLUTE flux bias (the probe sets the line's DC offset per point, so the window is DAC volts, not an excursion from idle_flux): tracks the dip at every flux and fits its flux dependence with a selectable model (analysis_method='dispersive' or 'sine'); proposes the sweet-spot flux (flux_offset) + flux period (flux_per_phi0) as physical facts on the qubit's flux channel, and sets the operating point at the sweet spot (the flux channel's idle_flux = flux_offset, the r…"""
    return run_scqo(
        "resonator_spectroscopy_flux",
        {
            "targets": targets,
            "flux_component": flux_component,
            "min_flux_v": min_flux_v,
            "max_flux_v": max_flux_v,
            "num_flux_points": num_flux_points,
            "num_averages": num_averages,
            "frequency_span_hz": frequency_span_hz,
            "num_freq_points": num_freq_points,
            "f_q_max_hz": f_q_max_hz,
            "analysis_method": analysis_method,
            "edge_margin_frac": edge_margin_frac,
            "dip_method": dip_method,
        },
    )
