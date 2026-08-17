"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_relaxation(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    min_wait_ns: float = 16,
    max_wait_ns: float = 200000,
    num_points: int = 51,
    thermalization_factor: float = 10.0,
) -> dict:
    """Excite with a pi pulse, wait a swept delay and measure; fits the exponential decay and proposes t1_s as a physical parameter (sample physics, no instrument knob) AND thermalization_factor x T1 as each target's thermalization_time_s knob — this is the experiment that calibrates the thermal-reset wait every other experiment uses. use_state_discrimination returns the FPGA-discriminated averaged state instead of I/Q (needs a calibrated discriminator: run single_shot_readout and accept its readout_r…"""
    return run_scqo(
        "qubit_relaxation",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "min_wait_ns": min_wait_ns,
            "max_wait_ns": max_wait_ns,
            "num_points": num_points,
            "thermalization_factor": thermalization_factor,
        },
    )
