# Verification of version 0.3.0

Executed locally on 1 October 2026 using Python 3.12.14.

- All 31 existing unit tests passed: 10 route, 10 experimental, 5 GPS and
  6 fuel-cost tests.
- All five README examples completed: experimental, GPS, route, general
  fuel cost and equal-gas-quality fuel cost. Each produced one JSON file and
  two nonempty CSV tables. Every JSON output identified version 0.3.0.
- A second execution of each command rejected existing output files with
  exit code 2. Output hashes confirmed that no result was overwritten.
- The equal-gas-quality example returned Diesel/CNG/Bio-CNG expenditures of
  48/36/40 RON and a 12 RON/kg break-even price for both gases. The 1.5
  Bio-CNG price factor returned 60 RON, or 25% above fixed Diesel expenditure.
  These are artificial example values, not OLGA campaign results.
- Calculation modules, tests and synthetic inputs are unchanged from the
  incoming snapshot; only the package version declaration changes in Python.
- SHA256SUMS.json was regenerated for all distributed source files other
  than itself, including the equal-quality example previously omitted.

Unit tests cover sample SD, missing/duplicate observations, undefined
relative differences, fuel-energy conservation, known spherical arcs,
interpolation, rejected extrapolation, invalid profile shares, timestamp
pairing, zero-distance GPS, nonpositive time intervals, expenditure thresholds
and consistent currency/tax units. Cost sensitivity holds Diesel fixed.

To rerun the unit tests:

```sh
python -m unittest discover -s tests -v
```

Use the five README example commands from the repository root, each with a
new output folder. Their results do not establish testing on every Python or
platform combination. No online prices, emissions certification, full OBD
calibration, independent drive-cycle validation or original DOCX-to-Excel
workflow were tested.

The earlier 0.3.0rc1 verification note reported private numerical comparisons.
Those checks are historical and were not repeated for this source update.
The present verification covers public synthetic examples only and does not
establish public availability of a GitHub release.
