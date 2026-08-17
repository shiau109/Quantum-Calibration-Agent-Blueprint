"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from _scqo_runtime import run_scqo


def scqo_resonator_spectroscopy_power_amp(
    targets: list,
    num_averages: int = 100,
    frequency_span_hz: float = 20000000.0,
    num_freq_points: int = 101,
    max_power_dbm: float = -20.0,
    min_power_dbm: float = -50.0,
    num_power_points: int = 21,
    readout_depletion_ns: float = None,
    dip_method: str = 'lorentzian',
) -> dict:
    """Fast punchout: solves the output chain for max_power_dbm once (recorded boundary write, reverted after), then sweeps the digital readout AMPLITUDE down from it in ONE hardware program. Same absolute-dBm window and proposals (readout_power_dbm + readout_freq_hz) as resonator_spectroscopy_power_chain, minutes faster; SNR is best near the top of the window and degrades toward the bottom (the chain-stepped sibling keeps amp ~0.5 at every point). Use for quick scans; use _chain for per-point-optimal…"""
    return run_scqo(
        "resonator_spectroscopy_power_amp",
        {
            "targets": targets,
            "num_averages": num_averages,
            "frequency_span_hz": frequency_span_hz,
            "num_freq_points": num_freq_points,
            "max_power_dbm": max_power_dbm,
            "min_power_dbm": min_power_dbm,
            "num_power_points": num_power_points,
            "readout_depletion_ns": readout_depletion_ns,
            "dip_method": dip_method,
        },
    )
