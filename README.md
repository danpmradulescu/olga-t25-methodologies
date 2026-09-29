# OLGA T2.5 reproducible calculation methods

Preparation candidate **0.3.0rc1**, 29 September 2026. Not a published release.
Licence and named software-contributor attribution are pending confirmation. No
open-source licence is granted by this preparation package. See LICENSE_STATUS.md.

This repository candidate documents three calculation components:

| Component | Executable | Documentation |
|---|---|---|
| A. Stationary Testo readings, dashboard fuel-energy conversion and timestamped GPS | `olga_route_model.experimental`, `olga_route_model.gps` | [Measurement method](docs/MEASUREMENT_METHOD.md) |
| B. Empirical common-route fuel, reference Bio-CNG and conditional GHG screening | `olga_route_model` | [Route method](docs/ROUTE_METHOD.md) |
| C. Optional illustrative fuel expenditure and price thresholds | `olga_route_model.fuel_cost` | [Fuel-cost method](docs/FUEL_COST_METHOD.md) |

“Hybrid” describes the combination of observed inputs, inherited estimates and
scenario assumptions. It does not mean hybrid-electric propulsion.

## Run the synthetic examples

Requires Python 3.10 or later. All executable modules use the Python standard
library. No pip installation, online service or paid library is needed. From
this directory, run each command once using a new output directory:

```sh
python -m unittest discover -s tests -v
python -m olga_route_model.experimental --input examples/experimental_synthetic.json --output run_measurements
python -m olga_route_model.gps --input examples/gps_synthetic.kml --output run_gps
python -m olga_route_model --input examples/synthetic.json --output run_route
python -m olga_route_model.fuel_cost --input examples/fuel_cost_synthetic.json --output run_cost
```

Each module writes JSON and CSV. See [inputs](docs/INPUT_OUTPUT.md),
[evidence and confidentiality](docs/DATA_POLICY.md), and
[verification](docs/VERIFICATION.md). Examples are artificial and do not reproduce
OLGA campaign results. Their fuel-property and reference constants are explicitly
specified assumptions, not measurements.

## Scientific scope

Component A calculates arithmetic means and sample standard deviations of
within-condition readings. It retains concentrations as concentrations. It does
not calculate g/km, g/kWh, oxygen-normalised emissions or significance tests.
The dashboard module converts supplied consumption values to energy. It does
not decode CAN signals or derive the unavailable upstream CNG OBD calibration.
The GPS module calculates interval speeds from timestamped coordinates.

Component B uses horizontal route geometry, linear interpolation of supplied
consumption curves and distance shares. Both movement-only and additive-idle
cases are retained. An idle allowance may overlap with effects already present
in a route-normalised consumption curve. Gradients, acceleration, payload,
auxiliaries and after-treatment dynamics are unresolved. Bio-CNG substitution
assumes equal gas-vehicle energy demand and unchanged efficiency. GHG results
require complete, documented life-cycle factors and are not a fuel certificate.

Component C multiplies fuel quantities by prices and explores assumed changes.
It is not a CBA, ownership-cost model or estimate of biomethane production cost.
It is a new optional extension, not retrospectively part of an earlier D2.8 draft.

## Provenance and status

The route and experimental calculation code extends the supplied v0.2.0 source
archive. The timestamped GPS component and optional fuel-cost component were
prepared in this candidate. The historical workbook source was inspected,
not rerun as a complete original document-to-workbook workflow. Details are in
[provenance](docs/PROVENANCE.md) and [alternatives](docs/ALTERNATIVES.md).

Software preparation and documentation used AI assistance. Responsibility for
scientific interpretation and release remains with the project contributors.
No consortium endorsement, software validation or public GitHub location is
claimed. [Release steps](docs/RELEASE.md) identify the remaining decisions.
