"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from _scqo_runtime import run_scqo


def scqo_resonator_spectroscopy_power_chain(
    targets: list,
    start_readout_detuning_hz: float = -10000000.0,
    end_readout_detuning_hz: float = 10000000.0,
    num_readout_freq_points: int = 101,
    num_averages: int = 100,
    max_power_dbm: float = -20.0,
    min_power_dbm: float = -50.0,
    num_power_points: int = 21,
    dip_method: str = 'lorentzian',
) -> dict:
    """Careful punchout that STEPS THE OUTPUT CHAIN (QM full_scale_power_dbm / Qblox output_att) per power point, holding the digital amplitude ~0.5 for best SNR (slow: one compile+run cycle per point; wide absolute range; cross-backend comparable). Absolute dBm axis; proposes readout_power_dbm + readout_freq_hz. Use for a calibrated wide sweep. (The sibling resonator_spectroscopy_power_amp is the fast amplitude-sweep version.) Also extracts the punchout's two branches as resonator-mode facts: the low…"""
    return run_scqo(
        "resonator_spectroscopy_power_chain",
        {
            "targets": targets,
            "start_readout_detuning_hz": start_readout_detuning_hz,
            "end_readout_detuning_hz": end_readout_detuning_hz,
            "num_readout_freq_points": num_readout_freq_points,
            "num_averages": num_averages,
            "max_power_dbm": max_power_dbm,
            "min_power_dbm": min_power_dbm,
            "num_power_points": num_power_points,
            "dip_method": dip_method,
        },
    )
