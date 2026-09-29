# Calculation method

## Scope and provenance

This is an empirical deterministic screening model. “Hybrid” refers to the combination of route geometry, recorded consumption indications, an inherited modelled curve and assumed operating conditions. It is not a simulation of hybrid-electric propulsion. The first OLGA route calculations used a spreadsheet; version 0.1.0 is a subsequent Python reimplementation, extended with composition and conditional GHG calculations. No calibration is fitted by this software.

## Geometry

For each consecutive KML longitude/latitude pair, use radians and

`h = sin²(Δlat/2) + cos(lat1) cos(lat2) sin²(Δlon/2)`

`d = 2 R asin(sqrt(h))`, with rounding clamped to `0 <= h <= 1`.

Sum segment distances with `R = 6371 km` by default. KML altitude and time are not used. Select a single LineString explicitly if several exist. An identical return leg is multiplication, not independently mapped geometry.

## Empirical consumption and time

For speed `v` between supplied adjacent curve nodes `(va, ca)` and `(vb, cb)`, use

`c(v) = ca + (cb - ca) (v - va) / (vb - va)`.

Extrapolation is rejected. For route distance `D` in km and distance fractions `wi` summing to 1:

`Fmove = D / 100 × Σ wi c(vi)`

`tmove = 60 D × Σ wi / vi` (minutes).

Consumption curves are in L/100 km (Diesel) and kg/100 km (CNG). Fractions are distance shares, not time shares. Optional curve factors are dimensionless user scenarios; default 1 introduces no refit.

`Fscreen = Fmove + qidle tidle / 60`.

Idle rates use L/h or kg/h, and stationary time uses minutes. Both cases are retained because the added stationary allowance can double-count effects in a route-calibrated curve. Accelerations, slopes, gears, passenger loads, HVAC and after-treatment transients are not resolved.

## Fuel energy and reference Bio-CNG

`QD = FD rhoD LHVD`; `QC = FC LHVC`, all energies in MJ.

The dry reference mixture contains CH4, CO2 and N2 with mole fractions summing to 1. Molar masses are 16.043, 44.010 and 28.014 kg/kmol, respectively. Only methane contributes heating value:

`Mmix = Σ yi Mi`

`wCH4 = yCH4 MCH4 / Mmix`

`LHVB = wCH4 LHVCH4`

`rhoB = Mmix / 22.41397` kg/Nm3 (ideal dry gas, 0 °C and 101.325 kPa).

Assume unchanged gas-vehicle efficiency: `QB = QC`, `FB = QC / LHVB`, `VB = FB / rhoB`.

Fuel conformity to EN 16723-2 requires more than bulk methane composition and is assumed, not tested. The calculation does not model compression storage or upgrade a lower-quality pilot gas. Fuel quality and sustainability certification are distinct.

## Conditional life-cycle GHG

For a **complete** intensity `E` in gCO2e/MJ, `G = Q E / 1000` kgCO2e.

With reference intensity `ER`, calculate separately:

- Fuel-energy saving: `1 - EB / ER`.
- Same-route saving against the Diesel-energy reference: `1 - QB EB / (QD ER)`.
- Break-even Bio-CNG intensity: `ER QD / QB`.

The OLGA scenario uses the RED transport comparator 94 gCO2e/MJ as a benchmark, not a measured Diesel supply-pathway factor. Hypothetical intensities are not regulatory pathway defaults. The supplied complete intensity must account for the chosen upstream and fuel-use boundary, including applicable non-CO2 emissions. Biogenic CO2 accounting does not mean physical exhaust CO2 is zero. Negative intensities are permitted mathematically but require a separately justified pathway and credit inventory.

Sensitivity multiplies total gas energy (including the chosen stationary allowance) by positive scenario factors while keeping Diesel energy fixed. This is a stress test, not a confidence interval. No fossil-CNG intensity is assumed by the program.

## Verification and references

Unit tests use analytically checkable cases, conservation of fuel energy, interpolation endpoints, known spherical arcs and invalid-input rejection. The private reproduction bundle compares the Python outputs with the earlier unrounded spreadsheet results. Agreement establishes numerical reproduction, not empirical validation.

Framework: Directive (EU) 2018/2001, Annex VI, https://eur-lex.europa.eu/eli/dir/2018/2001/oj ; JEC Well-to-Wheels v5, DOI 10.2760/100379. The code does not implement an official RED certification procedure or JEC pathway database. Specific scenario sources and their status must be recorded in the input evidence object.
