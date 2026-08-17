"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from typing import Annotated

from _scqo_runtime import run_scqo


def scqo_qubit_stark_phase_echo(
    targets: list,
    reset_method: str = 'thermal',
    thermalization_time_ns: float = None,
    active_reset_rounds: Annotated[int, (1, 15)] = 1,
    use_state_discrimination: bool = False,
    num_averages: int = 100,
    stark_operation: str = 'stark',
    stark_detuning_hz: float = 50000000.0,
    min_stark_amp: float = 0.0,
    max_stark_amp: float = 1.0,
    num_amp_points: int = 21,
) -> dict:
    """AC-Stark phase echo: a Hahn echo (X90 - wait(D) - X180 - stark(D) - close - readout) with an off-resonant Stark tone filling the second free-evolution arm (the first arm is an idle of the same duration D). The echo refocuses static dephasing, so the surviving phase is the AC-Stark shift the tone imprints. The phase is read in two bases (close with X90 -> sin(phi), -Y90 -> cos(phi)) so it is unambiguous, and only the tone's amplitude is swept; the estimator fits phi vs amp^2 to the Stark coeffic…"""
    return run_scqo(
        "qubit_stark_phase_echo",
        {
            "targets": targets,
            "reset_method": reset_method,
            "thermalization_time_ns": thermalization_time_ns,
            "active_reset_rounds": active_reset_rounds,
            "use_state_discrimination": use_state_discrimination,
            "num_averages": num_averages,
            "stark_operation": stark_operation,
            "stark_detuning_hz": stark_detuning_hz,
            "min_stark_amp": min_stark_amp,
            "max_stark_amp": max_stark_amp,
            "num_amp_points": num_amp_points,
        },
    )
