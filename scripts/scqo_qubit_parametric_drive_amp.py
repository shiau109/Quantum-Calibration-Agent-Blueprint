"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_parametric_drive_amp(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    start_parametric_amp_v: float = 0.0,
    end_parametric_amp_v: float = 0.3,
    num_amp_points: int = 21,
    start_parametric_freq_hz: float = 50000000.0,
    end_parametric_freq_hz: float = 300000000.0,
    num_freq_points: int = 51,
    drive_time_ns: int = 2000,
) -> dict:
    """Parametric-drive resonance map: excite the qubit, then modulate its own flux (z) line with an RF tone of swept frequency and amplitude for a FIXED user-given driving time, and read the qubit back. Where the modulation frequency matches a sideband condition with a coupled component the excitation parametrically transfers out of the qubit, so the 2D population map draws the resonance line(s) — the operating-parameter finder for parametric coupling (frequency locates the coupling condition, amplit…"""
    return run_scqo(
        "qubit_parametric_drive_amp",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "start_parametric_amp_v": start_parametric_amp_v,
            "end_parametric_amp_v": end_parametric_amp_v,
            "num_amp_points": num_amp_points,
            "start_parametric_freq_hz": start_parametric_freq_hz,
            "end_parametric_freq_hz": end_parametric_freq_hz,
            "num_freq_points": num_freq_points,
            "drive_time_ns": drive_time_ns,
        },
    )
