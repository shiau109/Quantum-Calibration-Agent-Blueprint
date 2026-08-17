# Calibration Workflow (single fixed-frequency transmon)

The standard bring-up chain on this stack. Each step's experiment proposes
the parameters the next step depends on — run in order, review suggestions
after each step, and have the operator accept them before depending on them.

| # | Experiment | Measures | Key outputs (fit / suggestions) |
|---|---|---|---|
| 1 | `scqo_resonator_spectroscopy` | Readout resonator dip | `f_r_hz`, `kappa_tot_hz`; proposes `readout_freq_hz`, depletion wait |
| 2 | `scqo_readout_power` | Readout power operating point | best power below punch-out |
| 3 | `scqo_readout_frequency` | Fine readout frequency | refined `readout_freq_hz` |
| 4 | `scqo_qubit_spectroscopy` | Qubit transition (two-tone) | `f_01_hz`; proposes `drive_freq_hz` |
| 5 | `scqo_qubit_power_rabi` | π-pulse amplitude | `pi_amp`; proposes drive amplitude |
| 6 | `scqo_qubit_ramsey` | Fine qubit frequency + T2* | detuning correction, `t2_star_s` |
| 7 | `scqo_qubit_relaxation` | T1 | `t1_s`; proposes thermalization time |
| 8 | `scqo_qubit_echo` | T2 echo | `t2_echo_s` |
| 9 | `scqo_single_shot_readout` | Readout discrimination | rotation/threshold; UNLOCKS `reset_method="active"` and state readout |

After step 9, advanced experiments become available: three-state readout
(`scqo_single_shot_readout_gef`), thermal population, parity switching,
benchmarking (`scqo_qubit_sqrb`, `scqo_qubit_deterministic_benchmarking`),
DRAG tuning, and the flux/pair families on devices that support them
(chipA's single fixed-frequency qubit does not).

Ground rules per step:

- Run with defaults first (`targets` only); tighten spans/points only when
  the default window misses the feature.
- A `failed` fit on a first attempt usually means the swept window missed —
  widen the span once. If it fails again, report rather than iterate.
- Compare fitted values against the previous accepted values (the
  suggestion's `before` field): an order-of-magnitude jump is a red flag to
  report, not a discovery to celebrate.
- On real hardware, get explicit user confirmation before each step of the
  chain; on the simulator you may run the chain autonomously when asked.
