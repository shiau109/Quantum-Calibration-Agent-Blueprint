"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""

from _scqo_runtime import run_scqo


def scqo_qubit_parity_switch_discrete(
    targets: list,
    use_state_discrimination: bool = False,
    record_time_s: float = 30.0,
    num_shots: int = None,
    max_num_shots: int = 1400000,
    idle_time_ns: float = None,
    max_derived_idle_ns: float = 20000,
    readout_depletion_ns: float = None,
    psd_model: str = 'constrained',
    cycle_period_ns: float = None,
) -> dict:
    """Two-measurement charge-parity monitor: per cycle M1 - depletion wait - x90 - idle - y90 - M2 - pad, repeated at the fixed period cycle_period_ns (None = minimal). M1 projects the qubit and M2 reads the parity mapping, so parity[i] = m1[i] XOR m2[i] WITHIN each cycle — no chain across cycles, which is what makes a slow cycle period safe: T1 or readout error between cycles shows up only as the p_intercycle_flip diagnostic and corrupts no parity sample (the continuous variant cannot slow down with…"""
    return run_scqo(
        "qubit_parity_switch_discrete",
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
            "cycle_period_ns": cycle_period_ns,
        },
    )
