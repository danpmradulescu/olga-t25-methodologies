# Existing tools and method selection

The choice below is an engineering judgement based on available inputs, not a
benchmark demonstrating superiority. None of the alternatives was run to
produce this package's numerical outputs.

| Tool | Appropriate role | Why this workflow did not require it |
|---|---|---|
| Python statistics | Means and sample SD | Actually used; standard definitions, combined with the other local processing steps [1] |
| R | Statistical analysis | Could reproduce the descriptive statistics; an additional runtime was unnecessary for this small deterministic calculation [2] |
| jamovi | Graphical statistical analysis | A valid alternative; a script provides a repeatable combined sequence for statistics, units and route outputs [3] |
| VECTO | Vehicle energy and CO2 simulation | Engine, transmission, resistance and auxiliary input information for the tested buses is incomplete; filling the gaps with generic data would add assumptions [4] |
| SUMO | Microscopic traffic simulation | The route geometry alone does not define a traffic scenario or recorded drive cycle. A calibrated network, demand and vehicle assumptions would be needed [5] |

For SUMO's PHEMlight implementation, the documentation states that only two
passenger-car emission classes are included publicly and further classes need
separate licensing. This is a dataset limitation of that implementation, not a
claim that all SUMO emissions options require paid licences [6].

The simplified JRC bus model is a relevant future alternative but was not
implemented: Broekaert et al., A Simplified CO2 and Fuel Consumption Model for
Buses Derived from VECTO Simulations (2021), doi:10.4271/2021-24-0075.

Spreadsheet formulas can reproduce the fuel-cost arithmetic. The small Python
extension keeps quantities, units, prices and sensitivity in one versioned
workflow; it does not claim methodological novelty.

Primary documentation consulted 29 September 2026:
1. https://docs.python.org/3/library/statistics.html
2. https://www.r-project.org/about.html
3. https://www.jamovi.org/about.html
4. https://climate.ec.europa.eu/areas-action/transport-decarbonisation/road-transport/vehicle-energy-consumption-calculation-tool-vecto_en
5. https://eclipse.dev/sumo/
6. https://eclipse.dev/sumo/docs/Models/Emissions/PHEMlight.html
