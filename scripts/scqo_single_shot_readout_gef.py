"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_single_shot_readout_gef(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_shots: int = 2000,
    readout_freq_shift_hz: float = 0.0,
) -> dict:
    """Prepare |g>, |e> and |f> and record every readout shot's I/Q point; a three-Gaussian mixture gives the per-state assignment fidelities (stored as the readout channel's fidelity_g/fidelity_e/fidelity_f monitors), the full 3x3 confusion matrix both counted and fitted (run-record only) and the three measured blob centers (stored as the channel's pos_* reference). Use it to quantify LEAKAGE — how much |f> a gate or a reset leaves behind — which a two-state readout silently folds into |e>. Preparing…"""
    return run_scqo(
        "single_shot_readout_gef",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_shots": num_shots,
            "readout_freq_shift_hz": readout_freq_shift_hz,
        },
    )
