# A. Measurement processing and GPS

## Stationary readings

For each selected operating category and vehicle, the experimental module
requires exactly three documented readings of CO, CO2, NO, reported NOx and
gas temperature. Common idle is a category, not proof of identical rpm or load.
Unpaired operating categories may be retained in input but are not compared.

For n readings, mean = sum(x)/n and sample SD =
sqrt(sum((x - mean)^2)/(n - 1)). Python statistics.mean/stdev implement these
standard definitions [S1]. SD describes dispersion of the repeated readings,
not a complete uncertainty budget or independent vehicle trials.

The module rejects missing selected values and duplicate vehicle/category/
replicate identifiers. It performs no smoothing, outlier removal, imputation,
oxygen normalisation or dry/wet correction. Units are ppm for CO/NO/NOx,
volume % for CO2 and degrees Celsius for temperature. Reported NOx is not
reconstructed from NO and NO2. Missing NO2 is not replaced by zero. O2 is
excluded from the comparative calculation. A recorded zero does not establish
zero mass emissions or an instrument detection limit.

Absolute difference = CNG mean - Diesel mean. For concentrations and a nonzero
Diesel denominator, relative difference (%) = 100 * difference / Diesel mean.
A CO2 absolute difference is in percentage points. A Celsius difference is
reported only in degrees; no percentage relative to the arbitrary Celsius zero
is produced. Concentration differences are not g/km reductions or causal fuel
comparisons. Exhaust flow and aligned operating information are unavailable.

## Consumption and energy

The caller supplies dashboard indications or inherited modelled fuel estimates
with explicit status. Actual speed and nominal target are retained separately.
The module does not average speed-point consumption values into a route total.

Full-route CNG consumption = 100 * measured mass / matched route distance,
in kg/100 km. The mass and distance must cover the same operating window.
Diesel energy per 100 km = consumption in L/100 km * density in kg/L * LHV
in MJ/kg. CNG energy per 100 km = consumption in kg/100 km * LHV in MJ/kg.
Fuel-property assumptions must be recorded and are not fuel certificates.

## OBD proxy limitation

The historical measurement documentation describes normalising a relative
fuel-rate proxy to a measured full-route mass. In general, if the proxy is P(t),
k = M / integral(P dt), and modelled fuel rate = k P(t). This fixes one integral
and does not uniquely validate a speed-dependent curve.

The inspected historical analysis script reads previously tabulated CNG
estimates. It does not derive them from OBD signals. Raw proxy time series,
scaling, alignment, interpolation and idle rules are missing from the available
upstream record. Consequently the package cannot independently reconstruct
that calibration. The optional normalise_proxy utility only demonstrates a
rectangle sum using caller-supplied interval-mean proxy rates and durations.
It is not represented as the historical integration algorithm.

## Timestamped GPS

The gps module reads one explicitly selected gx:Track with paired timestamps
and longitude/latitude/altitude tuples. With R = 6371 km, horizontal haversine
segment distance d and positive time difference dt yield v = 3600*d/dt km/h.
Accepted distances and durations are summed. Average speed is total distance
/ total accepted hours, not the arithmetic average of interval speeds.

Speed bins are [0,10), [10,20), ... [50,60), [60,infinity) km/h. Time shares and
distance shares have separate denominators. No filtering or smoothing is
performed. Nonpositive-duration intervals are skipped and identified; no gap
is bridged. Altitude extrema are descriptive, not gradient inputs.

The historical script truncated unmatched time/coordinate arrays and could
join multiple tracks. This version rejects unpaired entries and requires track
selection instead. On well-formed single tracks the equations are equivalent.
A zero-distance track returns null distance shares. The geometry-only common
route reader is separate: a LineString without timestamps cannot yield speed.

[S1]: https://docs.python.org/3/library/statistics.html
