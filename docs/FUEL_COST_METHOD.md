# C. Illustrative fuel-cost calculations

This optional extension concerns expenditure on delivered vehicle fuel only.
It is not a CBA, total ownership cost, payback or biomethane plant cost model.

## Inputs

Supply the same service distance and consumption boundary for all fuels.
Each row declares quantity, unit, quantity_source, quantity_status, unit_price,
price_unit, price_basis, price_status and price_source. Consumption is in L for
Diesel and kg for CNG/Bio-CNG. Prices use the same currency and must consistently
include or exclude VAT. The program rejects incompatible units and tax bases.
It does not fetch or validate market prices. Sources should specify station,
observation date, retrieval date, delivery basis and quotation/assumption status.
An access date is not necessarily a price-observation date.

## Equations

For quantity q, price p and common distance D:

- route fuel expenditure C = q*p;
- expenditure per km = C/D;
- difference from Diesel (%) = 100*(C/C_D - 1), positive for higher cost;
- price matching Diesel expenditure = C_D/q.

With consumption multiplier a and price multiplier b, gas expenditure is
C_gas(a,b) = a*b*q_gas*p_gas. Diesel remains fixed. These multipliers are
assumed stress tests, not distributions or statistical confidence intervals.

Movement-only and additive-stationary outputs are separate alternatives.
Choose one consistent boundary per run. Never add another idle term to the
already combined result. For sensitivity of the consumption model itself,
rerun the route model rather than treating a cost multiplier as a new traffic
simulation. No fuel discounts, incentives or VAT recovery are inferred.

## Synthetic example and report use

The example uses an artificial service and hypothetical prices. It is unrelated
to an Antares quotation, project bus test or OLGA pilot production cost.
For confidential reproduction, create an input outside this repository using
reviewed consumption outputs and documented prices. If reproducing a printed
table, state whether quantities were rounded before multiplication. Prefer
unrounded model outputs for new analysis and round only the displayed results.

Attribution in a report should describe a fuel-expenditure calculation, not a
new economic model. Environmental benefits and financial savings are separate
outputs. Capital, maintenance, production and infrastructure expenditure are
outside this module. Already included delivery/compression costs must not be
added twice in a subsequent analysis.

## Equal-quality gas scenario

To isolate the price effect, assume the same lower heating value, engine
efficiency and duty profile for CNG and Bio-CNG. Equal energy demand then gives
q_Bio-CNG = q_CNG. The caller must supply these equal quantities; this module
does not derive them from composition. Compliance with the same automotive
fuel standard does not guarantee identical heating values for every batch.
A reference mixture with a different heating value is a separate scenario.
Keep the selected movement-only or additive-stationary boundary consistent.

## Bio-CNG premiums and support mechanisms

A Bio-CNG price premium over fossil CNG is a reasonable baseline assumption
without fiscal relief or other support, rather than a universal market rule.
The IEA finds that average biomethane production costs exceed wholesale
natural-gas prices in most regions and discusses tax exemptions and other
support mechanisms [C1, Section 2.5, p. 56]. The European Commission identifies
upgrading incentives as a way to reduce biomethane production costs [C2].
This supports the cost context, not a fixed final vehicle-fuel price premium.
Feedstock, scale, delivery, compression, taxes and contracts affect prices;
production costs and wholesale prices are not pump-price quotations.

Represent an assumed premium r as p_Bio-CNG = p_CNG * (1 + r). With equal gas
quantities, expenditure has the same relative premium. Bio-CNG can nevertheless
remain cheaper than Diesel if q_gas * p_Bio-CNG < q_Diesel * p_Diesel.
Document any applicable incentive separately and count it only once.

## Diversification and climate benefits

These theoretical scenarios support informed consideration of alternative
fuels, particularly Bio-CNG. Compatible vehicles and reliable supply can help
protect operating margins when relative prices favour gas. Include adverse
price combinations as well as favourable ones. A single price observation does
not demonstrate lower expenditure volatility; contracts linked to the same gas
index may rise together. Vehicle investment and operating constraints require
separate assessment. A Diesel bus cannot automatically switch to gas.

Built-in sensitivity varies gas price and consumption while holding Diesel
fixed. To vary the Diesel price, run a separate input with that price changed.
Hold service quantities fixed when isolating price effects.

Bio-CNG may combine competitive fuel expenditure with lower life-cycle carbon
emissions and waste valorisation. Assess climate benefits separately through
the complete carbon-intensity and route-energy method in ROUTE_METHOD.md.
They depend on feedstock, production pathway, energy inputs and methane losses.
Equal heating values do not imply equal life-cycle carbon intensities, and
renewable origin alone does not establish a specific emissions reduction.
Do not transfer Bio-CNG climate benefits to fossil CNG. The Commission also
identifies biomethane supply diversification as a potential way to reduce
exposure to volatile natural-gas prices [C2].

## Additional synthetic example

From the repository root, use a new output directory:

```sh
python -m olga_route_model.fuel_cost --input examples/fuel_cost_equal_quality_synthetic.json --output run_cost_equal_quality
```

All inputs below are artificial, not project results or market observations.
The common service is 20 km; hypothetical prices consistently include VAT.

| Fuel | Quantity | Price | Trip expenditure | Change vs Diesel |
|---|---:|---:|---:|---:|
| Diesel | 6 L | 8 RON/L | 48 RON | Reference |
| CNG | 4 kg | 9 RON/kg | 36 RON | -25.0% |
| Bio-CNG | 4 kg | 10 RON/kg | 40 RON | -16.7% |

Bio-CNG costs 11.1% more than CNG but 16.7% less than Diesel in this example.
Both gases break even with Diesel at 12 RON/kg. A 1.5 Bio-CNG price factor gives
60 RON per trip, 25% above the fixed Diesel reference. No OLGA campaign data,
operator quotations or confidential report inputs are used in this example.

## Economic context references

[C1] IEA (2025). *Outlook for Biogas and Biomethane: A global geospatial
assessment*. Section 2.5, p. 56, Figure 2.9.
https://www.iea.org/reports/outlook-for-biogas-and-biomethane

[C2] European Commission, Directorate-General for Energy. *Biomethane*.
Sections on diversification and production costs.
https://energy.ec.europa.eu/topics/renewable-energy/bioenergy/biomethane_en

Accessed 30 September 2026. These sources do not provide the synthetic prices
above or replace supplier-specific evidence.
