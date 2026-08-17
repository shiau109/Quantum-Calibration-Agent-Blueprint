"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_single_shot_readout(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_shots: int = 2000,
) -> dict:
    """Prepare |g> and |e> and record every readout shot's I/Q point; a two-Gaussian mixture gives the per-state assignment fidelities (stored as the readout channel's fidelity_g/fidelity_e monitors), the confusion probabilities (run-record only) and the measured |g>/|e> blob centers (stored as the channel's pos_* reference). A driver that can discriminate additionally PROPOSES the readout channel's discriminator knobs (readout_rotation_rad / readout_threshold / readout_rus_threshold) as governed sugg…"""
    return run_scqo(
        "single_shot_readout",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_shots": num_shots,
        },
    )
