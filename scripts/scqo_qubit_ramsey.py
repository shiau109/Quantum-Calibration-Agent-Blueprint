"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_ramsey(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    frequency_detuning_hz: float = 1000000.0,
    min_idle_time_ns: float = 16,
    max_idle_time_ns: float = 4000,
    num_points: int = 101,
    ramsey_model: str = 'auto',
) -> dict:
    """Two pi/2 pulses separated by a swept idle time with an artificial drive detuning; fits the decaying fringe to correct the drive channel's drive_freq_hz and report T2*. A charge-parity-split fringe selects the two-frequency beat model (force it with ramsey_model='beat'): the drive retunes to the MEAN of the two branches and the splitting |f_1 - f_2| is proposed as the drive channel's parity_delta_f_hz monitor — the input the parity-switch monitors (qubit_parity_switch_continuous / qubit_parity_s…"""
    return run_scqo(
        "qubit_ramsey",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "frequency_detuning_hz": frequency_detuning_hz,
            "min_idle_time_ns": min_idle_time_ns,
            "max_idle_time_ns": max_idle_time_ns,
            "num_points": num_points,
            "ramsey_model": ramsey_model,
        },
    )
