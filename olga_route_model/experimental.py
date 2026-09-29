"""Reproduce tabulated Testo and dashboard post-processing, not instrument acquisition."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import statistics
import sys
from . import __version__
from .model import number

PARAMETERS = [('CO [ppm]', 'co_ppm'), ('CO2 [%]', 'co2_percent'),
              ('NO [ppm]', 'no_ppm'), ('NOx [ppm]', 'nox_ppm'),
              ('Gas temperature [°C]', 'gas_temperature_c')]


def describe(values):
    """Arithmetic mean and sample SD; no imputation or outlier deletion."""
    if len(values) < 2:
        raise ValueError('At least two finite observations are needed for sample SD')
    values = [number(v, 'observation') for v in values]
    return {'n': len(values), 'mean': statistics.mean(values), 'sample_sd': statistics.stdev(values)}


def normalise_proxy(intervals, measured_mass_kg):
    """Optional interval-mean proxy method; not a reconstruction of missing OLGA OBD data.

    Caller supplies complete interval-mean relative fuel rates and interval durations.
    A piecewise-constant rectangle sum is explicitly used. No GPS interpolation is
    inferred and no rpm/stroke conversion or engine configuration is assumed.
    """
    mass = number(measured_mass_kg, 'measured mass', positive=True)
    if not intervals:
        raise ValueError('A complete interval sequence is required')
    weights = [number(r['relative_rate'], 'relative rate', minimum=0)*
               number(r['duration_s'], 'duration', positive=True) for r in intervals]
    total = number(sum(weights), 'integrated proxy', positive=True)
    scale = mass/total
    return {'normalisation_kg_per_proxy_second': scale,
            'interval_modelled_mass_kg': [scale*w for w in weights],
            'integrated_modelled_mass_kg': scale*total,
            'method': 'interval-mean proxy rectangle sum; normalisation is not validation'}


def analyse(config):
    if config.get('schema_version') != 1:
        raise ValueError('Expected experimental schema_version 1')
    raw = config['stationary_readings']
    seen = set()
    for row in raw:
        key = (row['vehicle'], str(row['point']), row['rep'])
        if key in seen: raise ValueError('Duplicate vehicle/point/replicate identifier')
        seen.add(key)
    summaries = []
    for point in config['common_points']:
        grouped = {vehicle: [r for r in raw if r['vehicle']==vehicle and str(r['point'])==str(point)]
                   for vehicle in ('Diesel','CNG')}
        if any(len(rows)!=3 for rows in grouped.values()):
            raise ValueError('Exactly three readings per vehicle/common point required')
        for label,key in PARAMETERS:
            d=describe([r[key] for r in grouped['Diesel']]);c=describe([r[key] for r in grouped['CNG']])
            delta=c['mean']-d['mean']
            # Celsius zero is arbitrary. Report a temperature difference only.
            pct=100*delta/d['mean'] if key!='gas_temperature_c' and d['mean']!=0 else None
            summaries.append({'point':str(point),'parameter':label,'n_diesel':d['n'],'n_cng':c['n'],
                'diesel_mean':d['mean'],'diesel_sample_sd':d['sample_sd'],
                'cng_mean':c['mean'],'cng_sample_sd':c['sample_sd'],
                'difference_cng_minus_diesel':delta,'relative_concentration_difference_percent':pct,
                'interpretation':'Temperature difference in degC; no Celsius percentage.' if key=='gas_temperature_c'
                   else 'Descriptive concentration difference only; not mass emissions or a causal fuel effect.'})
    props=config['fuel_properties'];density=number(props['diesel_density_kg_l'],'density',positive=True)
    dl=number(props['diesel_lhv_mj_kg'],'Diesel LHV',positive=True)
    cl=number(props['cng_lhv_mj_kg'],'CNG LHV',positive=True)
    segments=[]
    for row in config['speed_segments']:
        v=row['vehicle']; expected='L/100 km' if v=='Diesel' else 'kg/100 km'
        if v not in ('Diesel','CNG') or row['unit']!=expected:
            raise ValueError('Unexpected vehicle or consumption unit')
        fuel=number(row['consumption'],'consumption',minimum=0)
        number(row['actual_speed_kmh'],'actual speed',positive=True)
        segments.append({**row,'energy_mj_100km':fuel*density*dl if v=='Diesel' else fuel*cl})
    route=config['cng_full_route']
    mass=number(route['measured_full_to_full_kg'],'CNG mass',positive=True)
    distance=number(route['derived_distance_km'],'CNG distance',positive=True)
    return {'software':'OLGA Route Model','version':__version__,'module':'experimental',
        'stationary_summary':summaries,'speed_segments':segments,
        'cng_route_kg_100km':100*mass/distance,
        'input_config_sha256':hashlib.sha256(json.dumps(config,sort_keys=True,allow_nan=False).encode()).hexdigest(),
        'evidence':config.get('evidence',{}),
        'exclusions':['O2 excluded from comparative interpretation.',
            'Missing Diesel NO2 is not zero; reported NOx is not reconstructed.',
            'Recorded zero concentrations are not certified zero emissions.',
            'No oxygen normalisation, dry/wet correction, g/km or g/kWh conversion.',
            'No route-total Diesel consumption or calibrated CNG curve fitting is inferred.',
            'Three repeats are within-condition readings, not three independent vehicle trials.']}


def main():
    p=argparse.ArgumentParser(description='Tabulated Testo and dashboard reproducibility module')
    p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    try:
        cfg=json.loads(a.input.read_text(encoding='utf-8'));r=analyse(cfg)
        r['execution']={'python_version':sys.version.split()[0],
            'input_file_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),
            'experimental_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        files=[a.output/n for n in ('experimental_results.json','stationary_summary.csv','energy_segments.csv')]
        if any(f.exists() for f in files):raise ValueError('Outputs already exist; choose a new directory')
        a.output.mkdir(parents=True,exist_ok=True)
        files[0].write_text(json.dumps(r,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        for file,rows in [(files[1],r['stationary_summary']),(files[2],r['speed_segments'])]:
            if not rows:raise ValueError('Missing output rows')
            with file.open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        print(f'Experimental results saved to {a.output}')
    except (ValueError,KeyError,TypeError,OSError) as exc:p.exit(2,f'Input/output error: {exc}\n')

if __name__=='__main__':main()
