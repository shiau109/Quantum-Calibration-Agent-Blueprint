"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_parametric_drive_time(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    parametric_amp_v: float = 0.15,
    start_parametric_freq_hz: float = 180000000.0,
    end_parametric_freq_hz: float = 220000000.0,
    num_freq_points: int = 21,
    start_drive_time_ns: float = 16.0,
    end_drive_time_ns: float = 3000.0,
    num_time_points: int = 101,
) -> dict:
    """Parametric-drive chevron: excite the qubit, then modulate its own flux (z) line with an RF tone of swept frequency at a FIXED user-given amplitude, hold it for a SWEPT driving time, and read the qubit back. Where the modulation frequency meets a sideband condition with a coupled component the excitation exchanges out of the qubit and back, so each frequency row is an oscillating rho_11(t) — the map is the chevron and the fit gives the coherent coupling rate, the loss rate and the exceptional-po…"""
    return run_scqo(
        "qubit_parametric_drive_time",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "parametric_amp_v": parametric_amp_v,
            "start_parametric_freq_hz": start_parametric_freq_hz,
            "end_parametric_freq_hz": end_parametric_freq_hz,
            "num_freq_points": num_freq_points,
            "start_drive_time_ns": start_drive_time_ns,
            "end_drive_time_ns": end_drive_time_ns,
            "num_time_points": num_time_points,
        },
    )
