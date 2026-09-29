"""Illustrative delivered-fuel expenditure; no CBA or ownership-cost model."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
from . import __version__
from .model import number


def calculate_costs(config):
    if config.get('schema_version') != 1:
        raise ValueError('Expected fuel-cost schema_version 1')
    distance = number(config['distance_km'], 'distance_km', positive=True)
    currency = config['currency']
    if not isinstance(currency, str) or not currency.strip():
        raise ValueError('Supply a common currency')
    basis = config['price_basis']
    if basis not in ('VAT_inclusive', 'VAT_exclusive'):
        raise ValueError('Declare one consistent price basis')
    if not config.get('assessment_date') or not config.get('consumption_boundary'):
        raise ValueError('Declare assessment date and consumption boundary')
    fuels = config['fuels']
    if set(fuels) != {'Diesel', 'CNG', 'Bio-CNG'}:
        raise ValueError('Supply Diesel, CNG and Bio-CNG')
    rows = []
    for name in ('Diesel', 'CNG', 'Bio-CNG'):
        f = fuels[name]
        unit = 'L' if name == 'Diesel' else 'kg'
        if f['quantity_unit'] != unit or f['price_unit'] != currency + '/' + unit:
            raise ValueError('Quantity and price units must match')
        if f['price_basis'] != basis:
            raise ValueError('Mixed tax bases are unsupported')
        if f['quantity_status'] not in ('measured', 'derived', 'modelled', 'synthetic'):
            raise ValueError('Declare quantity evidence status')
        if f['price_status'] not in ('external-reference', 'assumed', 'synthetic'):
            raise ValueError('Declare price evidence status')
        if not f.get('price_source') or not f.get('quantity_source'):
            raise ValueError('Document both sources, including synthetic assumptions')
        q = number(f['quantity'], 'quantity', positive=True)
        p = number(f['unit_price'], 'unit_price', positive=True)
        rows.append({'fuel': name, 'quantity': q, 'quantity_unit': unit,
                     'unit_price': p, 'price_unit': f['price_unit'],
                     'route_cost': q*p, 'cost_per_km': q*p/distance})
    baseline = rows[0]['route_cost']
    for row in rows:
        row['difference_vs_diesel_percent'] = 100*(row['route_cost']/baseline-1)
        row['price_for_equal_diesel_fuel_cost'] = baseline/row['quantity']
    sensitivities = []
    for qfactor in config['consumption_factors']:
        qfactor = number(qfactor, 'consumption factor', positive=True)
        for pfactor in config['price_factors']:
            pfactor = number(pfactor, 'price factor', positive=True)
            for row in rows[1:]:
                cost = row['route_cost']*qfactor*pfactor
                sensitivities.append({'fuel': row['fuel'], 'gas_consumption_factor': qfactor,
                    'gas_price_factor': pfactor, 'route_cost': cost,
                    'difference_vs_fixed_diesel_percent': 100*(cost/baseline-1)})
    if not sensitivities:
        raise ValueError('Sensitivity factor lists must be nonempty')
    return {'software': 'OLGA Route Model', 'version': __version__,
        'module': 'fuel_cost', 'scenario_id': config.get('scenario_id', ''),
        'assessment_date': config['assessment_date'], 'distance_km': distance,
        'currency': currency, 'price_basis': basis,
        'consumption_boundary': config['consumption_boundary'], 'inputs': config,
        'input_config_sha256': hashlib.sha256(json.dumps(config,sort_keys=True,allow_nan=False).encode()).hexdigest(),
        'fuel_costs': rows, 'sensitivity': sensitivities,
        'interpretation': ['Fuel expenditure only; no CBA, TCO, payback or plant-production costing.',
            'Positive percent difference means higher expenditure than Diesel.',
            'Sensitivity factors are assumptions, not confidence bounds.',
            'Use the same service, currency, tax and delivery boundary for every fuel.',
            'No price retrieval, tax recovery, incentive or fleet discount is inferred.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    try:
        raw = a.input.read_bytes()
        result = calculate_costs(json.loads(raw))
        result['execution'] = {'python_version': sys.version.split()[0],
            'input_file_sha256': hashlib.sha256(raw).hexdigest(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        files = [a.output/n for n in ('fuel_cost_results.json','fuel_costs.csv','sensitivity.csv')]
        if any(f.exists() for f in files):
            raise ValueError('Outputs already exist; choose a new directory')
        a.output.mkdir(parents=True, exist_ok=True)
        files[0].write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        for path, rows in zip(files[1:], (result['fuel_costs'],result['sensitivity'])):
            with path.open('w',newline='',encoding='utf-8') as stream:
                writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
                writer.writeheader(); writer.writerows(rows)
        print(f'Fuel-cost results saved to {a.output}')
    except (ValueError,KeyError,TypeError,OSError) as exc:
        p.exit(2,f'Input/output error: {exc}\n')


if __name__ == '__main__':
    main()
