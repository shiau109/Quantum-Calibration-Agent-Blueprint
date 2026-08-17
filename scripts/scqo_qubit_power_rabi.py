"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_power_rabi(
    targets: list,
    min_amp_factor: float = 0.0,
    max_amp_factor: Annotated[float, (0.0, 2.0)] = 1.9,
    num_amp_points: int = 101,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
) -> dict:
    """Sweep drive amplitude (as a factor of the current pi pulse) and fit the Rabi oscillation to recalibrate the drive channel's pi_amp. use_state_discrimination returns the FPGA-discriminated averaged state instead of I/Q (needs a calibrated discriminator: run single_shot_readout and accept its readout_rotation_rad / readout_threshold suggestions first)."""
    return run_scqo(
        "qubit_power_rabi",
        {
            "targets": targets,
            "min_amp_factor": min_amp_factor,
            "max_amp_factor": max_amp_factor,
            "num_amp_points": num_amp_points,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
        },
    )
