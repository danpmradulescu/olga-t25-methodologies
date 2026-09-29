# Verification of preparation candidate 0.3.0rc1

Executed 29 September 2026 using Python 3.12.14.

- 31 unit tests passed: 10 route, 10 experimental, 5 GPS and 6 fuel-cost tests.
- All four command-line examples completed, producing three files per module.
- JSON outputs parsed successfully and each CLI rejected overwriting results.
- Private numerical comparisons passed against the actual stored project
  workbooks and archived input mapping. Private values and execution files
  are deliberately excluded from this source tree.

Analytic tests cover sample SD, missing/duplicate observations, undefined
relative differences, energy conservation, known spherical arcs, interpolation,
no extrapolation, invalid profile shares, timestamp pairing, zero-distance GPS,
nonpositive time intervals, expenditure thresholds and consistent currency/tax
units. Cost sensitivity changes assumptions while holding Diesel fixed.

To rerun the unit tests:

```sh
python -m unittest discover -s tests -v
```

Use the four README commands for the example executions. This environment's
results do not establish testing on every supported Python/platform combination.
No live price API, emissions certification, original OBD calibration or validated
vehicle-dynamics simulation is part of these checks. No independent drive-cycle
validation or full original DOCX-to-Excel authoring run was performed.
