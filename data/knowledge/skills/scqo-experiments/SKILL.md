---
name: scqo-experiments
description: How to run, interpret, and troubleshoot scqo_* experiments (the SCQO lab-control stack). Read this BEFORE running any scqo_* experiment, interpreting its results, or troubleshooting a failure.
---

# SCQO Experiments

Every `scqo_*` experiment is a generated wrapper around one SCQO experiment.
The wrapper opens an SCQO session for the deployment this server was launched
with (sim / qblox / qm — see the system prompt banner), runs the experiment,
and returns SCQO's verdicts, fitted quantities, figures, and proposed
parameter updates. Full parameter tables: `documents/03_Experiment_API.md`.

## Running

1. `lab(action="schema", experiment_name="scqo_...")` for the real parameter
   names of THAT experiment. Never reuse parameter names from a different
   experiment or from an example in a document.
2. `targets` is always required: a list of component names from the device
   roster (e.g. `["q1"]`). Everything else has a sensible default — a first
   run with only `targets` is usually right.
3. Parameters documented "omit for backend default" default to null — leave
   them out entirely; never pass null explicitly.
4. `run_experiment(experiment_name="scqo_...", params={...})`. After it
   completes, ALWAYS show the plot tag: `<experiment experiment-id="ID" />`.

## Reading a result

| Field | Meaning |
|---|---|
| `status` | `success` = at least one target succeeded. NOT "all good" — check outcomes. |
| `results.outcomes` | Per-target verdict: `successful` / `failed` / `no_data`. |
| `results.record_outcome` | Collapsed verdict: `successful` / `partial` / `failed` / `no_data`. |
| `results.fit` | Fitted quantities per target (e.g. `f_r_hz`, `kappa_tot_hz`, `pi_amp`). |
| `results.suggestions` | SCQO's PROPOSED parameter updates — status `pending`, applied by a human, never by you. |
| `results.run_id` / `data_path` | The run's identity in the SCQO datastore (quote run_id when reporting). |
| `results.setup` | Which device/setup/backend actually executed — sanity-check this on every hardware run. |
| `error` | On failure: SCQO's structured message, verbatim. |

When you report a run: verdicts per target, the key fitted numbers with
units, then the suggestions as a table (entity, field, before → after) with
an explicit "pending — apply via the SCQO CLI if accepted" note.

## Calibration order (single fixed-frequency transmon)

resonator spectroscopy → readout power/frequency → qubit spectroscopy →
power rabi → ramsey (fine frequency) → relaxation (T1) → echo (T2) →
single-shot readout → (then: active reset becomes available; three-state
readout; parity/benchmarking experiments as needed).

Prerequisite chains that BLOCK experiments (refused by name, never silently
downgraded): `reset_method="active"` and state-discrimination options need
an accepted `scqo_single_shot_readout` first. The experiment descriptions in
03_Experiment_API.md name their own prerequisites — read them.

## Simulator notes (deployment `config.sim`)

- Runs execute offline against SCQO's simulated backend but persist real run
  folders (device chipA, setup `simulated`, tagged `qca`).
- `scqo_resonator_spectroscopy`: keep `analysis_method="lorentzian"` — the
  sim's phase quadrature is pure noise, so the `circle` fit fails BY DESIGN.
  That failure is expected behaviour, not a bug to fix.
- Identical parameters give identical data (deterministic seed) — reruns
  reproducing the same numbers is correct, not suspicious.

## Common failures

- **`invalid parameters for '...'` with a pydantic message**: a typo or a
  wrong value; the message names the field and the allowed values. Fix
  exactly what it names and retry once. Parameters not in the schema DO NOT
  EXIST — never invent one.
- **`Unknown parameter: X` (from the tool itself)**: same — call
  `lab(action="schema")` and use only listed names.
- **Unknown target**: use roster names from the error/schema; on chipA the
  qubit is `q1`.
- **Every target `no_data` / connection errors on hardware**: instrument or
  session problem — stop and report; do not retry-loop.
- **QM run appears hung, then times out "left running (detach)"**: the
  gateway may be busy or wedged (a notebook kernel can hold the connection).
  Operator escalation. Do not start another experiment.
- **`SCQO_AGENT_PYTHON is not set`**: the server was started without a
  launch script — tell the user to start via `launch/run-*.ps1`.
- **Figures missing but run succeeded**: report the run and mention the
  missing figures; they live under `results.data_path` in the SCQO store.

## What you never do

- Never pass `update` anywhere — it does not exist in the wrappers; runs are
  suggest-only by construction.
- Never claim a suggestion was applied; never present a proposed value as
  the device's current value.
- Never hand-roll a subprocess, interpreter path, or import workaround when
  a run fails — report the error instead.
