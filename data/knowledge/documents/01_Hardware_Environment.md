# Hardware Environment

This agent drives an SCQO-controlled superconducting-qubit lab. Which
instrument (if any) executes your experiments is fixed at server launch by
the SCQO deployment (see the system prompt banner) — you cannot switch
backends from inside a session.

## Deployments

| Deployment | Backend | What runs | Timeout policy |
|---|---|---|---|
| `config.sim` | SCQO simulated backend | Offline synthetic data, full pipeline | kill (safe) |
| `config.qblox` | Qblox cluster | REAL hardware (chipA on the qblox setup) | kill (cluster sockets release on exit) |
| `config.qm` | Quantum Machines OPX1000 | REAL hardware (chipA on qm_OPX1000) | **detach** — a timed-out child is left running to avoid orphaning the gateway job |

## Device: chipA

- Single fixed-frequency transmon, component name **`q1`** (this is the only
  valid entry in `targets` on this device).
- Associated components (roster-derived): `q1_res` (resonator), `q1_ro`
  (readout channel), drive channel — suggestions name these entities.
- Runs persist to the SCQO datastore at `D:/qpu_data_dev/chipA/<date>/<run_id>/`,
  tagged `qca`, with the QCA experiment id in the run note (`qca:<id>`).

## Provenance

Each QCA experiment record stores the SCQO `run_id` (in `results.run_id`)
and each SCQO run note carries the QCA experiment id, so runs can be
cross-referenced in both systems. The SCQO datastore — not QCA's HDF5
mirror — is the lab's source of truth.

## Known operational hazards

- **QM gateway wedge**: killing a QM run mid-job orphans the instrument-side
  job; the next run waits ~120 s and fails. Only an operator cluster restart
  clears it. This is why the qm deployment detaches on timeout and why you
  never run two experiments concurrently.
- **Qblox cluster sharing**: a live notebook kernel holding the cluster can
  garble concurrent connections. If runs start failing with connection
  errors, an open notebook is the first suspect — report, don't retry.
