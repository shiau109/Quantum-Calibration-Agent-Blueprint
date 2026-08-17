"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_xyz_delay(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    half_scan_ns: int = 60,
    z_pulse_amp_v: float = 0.1,
) -> dict:
    """Slide a fixed X180 XY pulse and a same-length Z (flux) pulse past each other at 1 ns resolution for two preparations (|e> via x180, |g> via idle) and fit the |e> - |g> contrast to the triangle overlap of the two pulses; its peak is the flux line's delay relative to the drive line, written to the flux channel's flux_delay_s so simultaneous XY+Z gates actually coincide. Needs a calibrated x180 (its length sets the triangle width). use_state_discrimination returns the FPGA-discriminated averaged s…"""
    return run_scqo(
        "qubit_xyz_delay",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "half_scan_ns": half_scan_ns,
            "z_pulse_amp_v": z_pulse_amp_v,
        },
    )
