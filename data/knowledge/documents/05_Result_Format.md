# Result Format (scqo_* experiments)

Every `scqo_*` run returns one dictionary with this exact shape:

```json
{
  "status": "success | failed",
  "error": "<only when failed: SCQO's structured message, verbatim>",
  "results": {
    "run_id": "20260817-...-chipA-resonator_spectroscopy-01",
    "data_path": "D:/qpu_data_dev/chipA/...",
    "setup": {"device": "chipA", "setup": "simulated", "backend": "simulated",
               "cooldown": "cd1", "config": "..."},
    "outcomes": {"q1": "successful"},
    "record_outcome": "successful | partial | failed | no_data",
    "fit": {"q1": {"f_r_hz": 5940886758.27, "kappa_tot_hz": 3568884.89}},
    "suggestions": [
      {"entity": "q1_ro", "field": "readout_freq_hz", "role": "knob",
       "unit": "Hz", "before": 5940000000.0, "after": 5940886758.27,
       "status": "pending"}
    ],
    "update_mode": "suggest"
  },
  "arrays": {"coord__detuning_hz": "...", "q1__I": "...", "q1__Q": "..."},
  "plots": [{"name": "q1__resonator_spectroscopy", "format": "png", "data": "<base64>"}]
}
```

Semantics:

- `status: "success"` = **at least one** target succeeded. Per-target truth
  is `results.outcomes`; the collapsed verdict is `results.record_outcome`
  (`partial` means a mixed run).
- `results.fit` holds the fitted physical quantities per target; names carry
  units (`_hz`, `_s`, `_ns`, `_dbm`).
- `results.suggestions` are SCQO's PROPOSED writebacks (`status: "pending"`).
  Nothing has been written to the device. A human reviews and accepts them
  with the SCQO CLI. Report them as a before → after table.
- `arrays` are 1-D slices of the run's dataset (sweep coordinate plus each
  target's signals), sized for `lab(action="get_array"/"get_stats")`.
  The complete dataset is `dataset.nc` inside `results.data_path`.
- `plots` are the SCQO estimator figures (PNG). Always display them with
  the `<experiment experiment-id="..." />` tag.
- A failed run may still carry partial `results` (e.g. outcomes and a
  `scqo_error`) — report what is there.
- `results.datastore_error`, if present, means the measurement succeeded but
  saving to the SCQO store failed — surface it prominently.
- A timeout under the qm deployment returns `status: "failed"` with
  `results.detached_pid`: the experiment child is STILL RUNNING. Operator
  escalation; never retry.
