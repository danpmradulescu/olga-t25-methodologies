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
