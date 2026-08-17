"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_echo(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    min_wait_ns: float = 32,
    max_wait_ns: float = 400000,
    num_points: int = 51,
) -> dict:
    """Hahn echo (X90 - tau/2 - X - tau/2 - X90) over a swept total idle time; fits the exponential envelope and proposes t2_echo_s as a physical parameter (sample physics, no instrument knob). use_state_discrimination returns the FPGA-discriminated averaged state instead of I/Q (needs a calibrated discriminator: run single_shot_readout and accept its readout_rotation_rad / readout_threshold suggestions first)."""
    return run_scqo(
        "qubit_echo",
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
        },
    )
