# Executable inputs and outputs

All JSON files use schema_version 1. Inputs are explicit, finite numeric values;
there is no automatic inference of measured status. See the examples for exact
field names. Run from the repository root with a new output folder.

## A. Experimental processing

`python -m olga_route_model.experimental --input INPUT.json --output OUTPUT`

Top-level fields: stationary_readings, common_points, speed_segments,
fuel_properties, cng_full_route and evidence. The synthetic example defines the
required keys. Replicates must be unique per vehicle and operating category.
Speed rows keep actual_speed_kmh and target_kmh separate; unit is exactly
`L/100 km` for Diesel or `kg/100 km` for CNG. Original files are not parsed by
this module: transcription into the input schema must be independently checked.

Outputs: experimental_results.json, stationary_summary.csv, energy_segments.csv.
O2 and NO2 may be retained in the input but are not compared or imputed.
An input can contain additional non-common categories; the selected categories
alone enter the paired descriptive summary.

## A. Timestamped GPS

`python -m olga_route_model.gps --input TRACK.kml --output OUTPUT`

If needed, add `--track-index 0` (zero-based). The file must contain gx:Track
with explicit timezone timestamps and one matching coordinate per timestamp.
Outputs: gps_results.json, gps_intervals.csv, gps_speed_bins.csv. Only the chosen
track is processed. No road matching or coordinate smoothing is performed.

## B. Route screening

`python -m olga_route_model --input INPUT.json --output OUTPUT`

Optional `--kml ROUTE.kml --line-index 0` replaces the distance with the selected
LineString length. This is a different geometry-only reader from A.
See [route input fields](ROUTE_INPUTS.md). Outputs: results.json, profile.csv,
summary.csv. Output distinguishes one_leg and identical_legs_total, and
movement_only from with_stationary_allowance. No automatic return mapping.

## C. Fuel expenditure

`python -m olga_route_model.fuel_cost --input INPUT.json --output OUTPUT`

See [cost method](FUEL_COST_METHOD.md) and examples/fuel_cost_synthetic.json.
Outputs: fuel_cost_results.json, fuel_costs.csv, sensitivity.csv. Quantity and
price status are retained. Positive differences mean higher cost than Diesel.

The CLIs refuse to overwrite existing result files. JSON records version and
input/source hashes. Hashes are identity checks, not scientific validation.
Only code and public examples belong in this repository; private inputs and
outputs must be stored outside it.
