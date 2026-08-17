"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_echo_flux_pulse(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    min_flux_v: float = -0.08,
    max_flux_v: float = 0.08,
    num_flux_points: int = 21,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    min_wait_ns: float = 32.0,
    max_wait_ns: float = 40000.0,
    num_wait_points: int = 51,
) -> dict:
    """Sweep a Z PULSE amplitude — RELATIVE to the flux channel's idle_flux, 0 = stay parked — and a total wait delay in a Hahn echo sequence, fitting T2_echo decay at each flux point to map out the T2_echo spectrum. Record-only: the fits are saved, nothing is proposed."""
    return run_scqo(
        "qubit_echo_flux_pulse",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "min_flux_v": min_flux_v,
            "max_flux_v": max_flux_v,
            "num_flux_points": num_flux_points,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "min_wait_ns": min_wait_ns,
            "max_wait_ns": max_wait_ns,
            "num_wait_points": num_wait_points,
        },
    )
