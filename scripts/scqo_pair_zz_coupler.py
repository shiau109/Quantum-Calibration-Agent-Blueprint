"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_pair_zz_coupler(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    num_averages: int = 100,
    min_coupler_v: float = -0.3,
    max_coupler_v: float = 0.3,
    num_coupler_points: int = 31,
    max_idle_time_ns: float = 4000,
    num_time_points: int = 41,
    detuning_hz: float = 1000000.0,
    measure: str = 'low',
) -> dict:
    """Residual-ZZ vs coupler standing bias (echo fringe under a virtual detuning, one pair member measured): finds the signed ZZ zero crossing and proposes it as idle_flux on the coupler's flux channel (the interaction-OFF standing bias); the residual zz_hz at the new point lands on the pair as a physical fact."""
    return run_scqo(
        "pair_zz_coupler",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "num_averages": num_averages,
            "min_coupler_v": min_coupler_v,
            "max_coupler_v": max_coupler_v,
            "num_coupler_points": num_coupler_points,
            "max_idle_time_ns": max_idle_time_ns,
            "num_time_points": num_time_points,
            "detuning_hz": detuning_hz,
            "measure": measure,
        },
    )
