"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_readout_frequency(
    targets: list,
    readout_mode: str = 'shot',
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    frequency_span_hz: float = 5000000.0,
    num_freq_points: int = 21,
    num_shots: int = 1000,
) -> dict:
    """Sweep the readout detuning reading |g> and |e>; picks the best frequency and updates the readout channel's readout_freq_hz. readout_mode='shot' records every shot's I/Q and optimizes single-shot FIDELITY; readout_mode='average' takes one FPGA-averaged I/Q point per prepared state and optimizes blob SEPARATION instead — faster, and it peaks at the same detuning."""
    return run_scqo(
        "readout_frequency",
        {
            "targets": targets,
            "readout_mode": readout_mode,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "frequency_span_hz": frequency_span_hz,
            "num_freq_points": num_freq_points,
            "num_shots": num_shots,
        },
    )
