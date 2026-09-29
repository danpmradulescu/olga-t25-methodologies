# Input format

The complete machine-readable example is `examples/synthetic.json`; all its vehicle and route values are synthetic. Schema version is 1. JSON numbers must be finite. Unknown metadata is not interpreted as model input.

| Field | Meaning and units |
|---|---|
| `route.one_way_distance_km` | Positive horizontal distance, replaced if `--kml` is supplied |
| `route.earth_radius_km` | Optional KML distance radius, default 6371 km |
| `identical_legs` | Positive integer; all per-leg totals multiplied by it |
| `distance_profile` | Nonempty list of `speed_kmh`, `distance_fraction`; positive speeds, nonnegative fractions summing to 1 |
| `diesel.curve`, `cng.curve` | Increasing pairs `[speed_kmh, consumption]`; L/100 km or kg/100 km; no extrapolation |
| `curve_factor` in each fuel | Optional positive dimensionless multiplier, default 1 |
| `diesel.density_kg_l` | Positive fuel density |
| `lhv_mj_kg` in each fuel | Positive lower heating value |
| `stationary_allowance` | Nonnegative `minutes_per_leg`, `diesel_l_h`, `cng_kg_h` |
| `biocng.dry_mole_fractions` | Exactly CH4, CO2, N2, nonnegative, sum 1 and CH4 positive |
| `biocng.methane_lhv_mj_kg` | Pure-methane LHV used for mixture |
| `ghg.reference_gco2e_mj` | Positive comparison intensity |
| `ghg.biocng_complete_gco2e_mj` | Nonempty list of complete life-cycle scenario intensities |
| `ghg.sensitivity_intensity_gco2e_mj` | Complete intensity held fixed for energy sensitivity |
| `ghg.gas_energy_factors` | Positive scenario multipliers for total gas energy |
| `scenario_id`, `evidence` | Identifiers and measured / derived / modelled / external-reference provenance |

This version supports positive total energy demand; zero-energy vehicles are outside scope. It does not infer measurement status from the numbers. Review each input's evidence and units. Input-file and canonical-configuration hashes identify distinct representations; a separate KML hash identifies the optional distance override.
