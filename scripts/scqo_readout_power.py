"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_readout_power(
    targets: list,
    min_amp_factor: float = 0.4,
    max_amp_factor: Annotated[float, (0.0, 2.0)] = 1.8,
    num_amp_points: int = 16,
    readout_mode: str = 'shot',
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_shots: int = 1000,
) -> dict:
    """Sweep the readout-amplitude prefactor reading |g> and |e>; picks the best amplitude and updates the readout channel's readout_amp. readout_mode='shot' records every shot's I/Q and optimizes single-shot FIDELITY; readout_mode='average' takes one FPGA-averaged I/Q point per prepared state and optimizes blob SEPARATION instead — faster, but blind to the measurement-induced transitions that limit the amplitude."""
    return run_scqo(
        "readout_power",
        {
            "targets": targets,
            "min_amp_factor": min_amp_factor,
            "max_amp_factor": max_amp_factor,
            "num_amp_points": num_amp_points,
            "readout_mode": readout_mode,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_shots": num_shots,
        },
    )
