"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from _scqo_runtime import run_scqo


def scqo_qubit_parity_switch_continuous(
    targets: list,
    use_state_discrimination: bool = False,
    record_time_s: float = 30.0,
    num_shots: int = None,
    max_num_shots: int = 2000000,
    idle_time_ns: float = None,
    max_derived_idle_ns: float = 20000,
    readout_depletion_ns: float = None,
    psd_model: str = 'constrained',
    idle_multiple: int = 1,
) -> dict:
    """Fixed-sequence charge-parity monitor: y90 - idle - x90 - measure repeated as back-to-back single shots for record_time_s (the shot count is derived from it, since the spectrum's lowest frequency is 8 / record_time_s and THAT is what sets how slow a rate is measurable), idle = 1 / (2 x parity_delta_f_hz) (the drive channel's stored beat splitting from a ramsey_model='beat' qubit_ramsey; +/- pi/2 parity phase), with ONLY the resonator depletion wait between shots — deliberately NO qubit reset, wh…"""
    return run_scqo(
        "qubit_parity_switch_continuous",
        {
            "targets": targets,
            "use_state_discrimination": use_state_discrimination,
            "record_time_s": record_time_s,
            "num_shots": num_shots,
            "max_num_shots": max_num_shots,
            "idle_time_ns": idle_time_ns,
            "max_derived_idle_ns": max_derived_idle_ns,
            "readout_depletion_ns": readout_depletion_ns,
            "psd_model": psd_model,
            "idle_multiple": idle_multiple,
        },
    )
