"""Pure calculation functions. Units are explicit; no fitting is performed here."""
from bisect import bisect_left
import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from . import __version__


def number(value, name, minimum=None, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return value


def haversine_km(a, b, radius_km=6371.0):
    """a and b are (longitude, latitude) degrees; horizontal spherical distance."""
    radius = number(radius_km, "radius_km", positive=True)
    for point in (a, b):
        lon, lat = point
        number(lon, "longitude"); number(lat, "latitude")
        if not -180 <= lon <= 180 or not -90 <= lat <= 90:
            raise ValueError("Coordinate outside longitude/latitude range")
    lon1, lat1, lon2, lat2 = map(math.radians, (*a, *b))
    h = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    return 2 * radius * math.asin(math.sqrt(min(1.0, max(0.0, h))))


def kml_route(path, line_index=None, radius_km=6371.0):
    """Read one LineString. Multiple lines require explicit zero-based selection.

    Only coordinate geometry is used; elevations and times are not inferred.
    XML is parsed locally, without retrieving URLs or external resources.
    """
    data = Path(path).read_bytes()
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError("KML document type and entity declarations are unsupported")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid KML XML: {exc}") from exc
    lines = [e for e in root.iter() if e.tag.split('}')[-1] == 'LineString']
    if not lines:
        raise ValueError("No KML LineString found")
    if line_index is None:
        if len(lines) != 1:
            raise ValueError("Multiple LineStrings: specify --line-index explicitly")
        line_index = 0
    if not 0 <= line_index < len(lines):
        raise ValueError("LineString index out of range")
    coords = [e for e in lines[line_index].iter() if e.tag.split('}')[-1] == 'coordinates']
    if len(coords) != 1:
        raise ValueError("Selected LineString must have one coordinates element")
    points = []
    for token in (coords[0].text or '').split():
        fields = token.split(',')
        if len(fields) < 2:
            raise ValueError("Invalid KML coordinate")
        points.append((float(fields[0]), float(fields[1])))
    if len(points) < 2:
        raise ValueError("At least two coordinates are required")
    distance = math.fsum(haversine_km(a, b, radius_km) for a, b in zip(points, points[1:]))
    number(distance, "route distance", positive=True)
    return {"one_way_distance_km": distance, "coordinate_count": len(points),
            "line_index": line_index, "earth_radius_km": radius_km,
            "kml_sha256": hashlib.sha256(data).hexdigest(),
            "geometry_status": "derived horizontal distance; no reverse-route validation"}


def validate_curve(curve):
    if len(curve) < 2:
        raise ValueError("At least two curve points are required")
    previous = -math.inf
    for speed, consumption in curve:
        speed = number(speed, "curve speed", positive=True)
        number(consumption, "curve consumption", minimum=0)
        if speed <= previous:
            raise ValueError("Curve speeds must be strictly increasing")
        previous = speed


def interpolate(curve, speed):
    """Piecewise linear interpolation. Extrapolation is deliberately rejected."""
    validate_curve(curve)
    speed = number(speed, "speed", positive=True)
    xs = [p[0] for p in curve]
    if not xs[0] <= speed <= xs[-1]:
        raise ValueError("Speed outside the supplied consumption curve")
    i = bisect_left(xs, speed)
    if xs[i] == speed:
        return float(curve[i][1])
    x0, y0 = curve[i-1]; x1, y1 = curve[i]
    return y0 + (y1-y0) * (speed-x0) / (x1-x0)


def mixture_properties(mixture):
    fractions = mixture['dry_mole_fractions']
    if set(fractions) != {'CH4', 'CO2', 'N2'}:
        raise ValueError("Reference mixture must explicitly contain CH4, CO2 and N2 only")
    for name, value in fractions.items():
        number(value, name + " mole fraction", minimum=0)
    if not math.isclose(math.fsum(fractions.values()), 1.0, rel_tol=0, abs_tol=1e-9):
        raise ValueError("Mole fractions must sum to one")
    number(fractions['CH4'], "CH4 mole fraction", positive=True)
    masses = {'CH4': 16.043, 'CO2': 44.010, 'N2': 28.014}
    molar_mass = math.fsum(fractions[k] * masses[k] for k in masses)
    w = fractions['CH4'] * masses['CH4'] / molar_mass
    lhv = number(mixture['methane_lhv_mj_kg'], "methane LHV", positive=True) * w
    density = molar_mass / 22.41397
    return {'molar_mass_kg_kmol': molar_mass, 'methane_mass_fraction': w,
            'lhv_mj_kg': lhv, 'normal_density_kg_nm3': density,
            'normal_lhv_mj_nm3': lhv*density,
            'normal_volume_basis': 'ideal dry gas, 0 degC, 101.325 kPa',
            'quality_status': 'fuel conformity assumed; not certified by this calculation'}


def calculate(config, route_override=None):
    if config.get('schema_version') != 1:
        raise ValueError("Unsupported schema_version (expected 1)")
    route = dict(route_override if route_override is not None else config['route'])
    distance = number(route['one_way_distance_km'], 'one_way_distance_km', positive=True)
    legs = number(config['identical_legs'], 'identical_legs', positive=True)
    if not legs.is_integer():
        raise ValueError('identical_legs must be an integer')
    profile = config['distance_profile']
    if not profile:
        raise ValueError('distance_profile must not be empty')
    for row in profile:
        number(row['speed_kmh'], 'profile speed', positive=True)
        number(row['distance_fraction'], 'distance fraction', minimum=0)
    if not math.isclose(math.fsum(r['distance_fraction'] for r in profile), 1, rel_tol=0, abs_tol=1e-9):
        raise ValueError('Distance fractions must sum to one')
    diesel = config['diesel']; cng = config['cng']
    dscale = number(diesel.get('curve_factor', 1), 'diesel curve factor', positive=True)
    cscale = number(cng.get('curve_factor', 1), 'cng curve factor', positive=True)
    rows = []
    for row in profile:
        speed, fraction = row['speed_kmh'], row['distance_fraction']
        dc = interpolate(diesel['curve'], speed) * dscale
        cc = interpolate(cng['curve'], speed) * cscale
        d = distance * fraction
        rows.append({'speed_kmh': speed, 'distance_fraction': fraction,
                     'distance_km': d, 'moving_min': 60*d/speed,
                     'diesel_l_per_100km': dc, 'cng_kg_per_100km': cc,
                     'diesel_l': d*dc/100, 'cng_kg': d*cc/100})
    dmove = math.fsum(r['diesel_l'] for r in rows)
    cmove = math.fsum(r['cng_kg'] for r in rows)
    tmove = math.fsum(r['moving_min'] for r in rows)
    idle = config['stationary_allowance']
    tidle = number(idle['minutes_per_leg'], 'stationary minutes', minimum=0)
    di = number(idle['diesel_l_h'], 'diesel idle rate', minimum=0)*tidle/60
    ci = number(idle['cng_kg_h'], 'CNG idle rate', minimum=0)*tidle/60
    de = number(diesel['density_kg_l'], 'diesel density', positive=True)*number(diesel['lhv_mj_kg'], 'diesel LHV', positive=True)
    ce = number(cng['lhv_mj_kg'], 'CNG LHV', positive=True)
    fuel = mixture_properties(config['biocng'])
    cases = {}
    for name, dm, cm, duration in [('movement_only', dmove, cmove, tmove),
                                  ('with_stationary_allowance', dmove+di, cmove+ci, tmove+tidle)]:
        qd, qc = dm*de, cm*ce
        number(qd, 'diesel route energy', positive=True)
        number(qc, 'gas route energy', positive=True)
        bm = qc/fuel['lhv_mj_kg']
        one = {'distance_km': distance, 'duration_min': duration,
               'diesel_l': dm, 'cng_kg': cm, 'biocng_kg': bm,
               'diesel_mj': qd, 'cng_mj': qc, 'biocng_mj': qc,
               'biocng_nm3': bm/fuel['normal_density_kg_nm3']}
        cases[name] = {'one_leg': one, 'identical_legs_total': {k:v*legs for k,v in one.items()}}
    ghg = config['ghg']
    reference = number(ghg['reference_gco2e_mj'], 'reference intensity', positive=True)
    ci_values = [number(x, 'Bio-CNG intensity') for x in ghg['biocng_complete_gco2e_mj']]
    if not ci_values:
        raise ValueError('At least one Bio-CNG intensity is required')
    for case in cases.values():
        qd = case['one_leg']['diesel_mj']; qb = case['one_leg']['biocng_mj']
        baseline = qd*reference/1000
        case['ghg'] = {'diesel_energy_reference_kgco2e_per_leg': baseline,
            'gas_to_diesel_energy_ratio': qb/qd,
            'biocng_break_even_gco2e_mj': reference*qd/qb,
            'scenarios': [{'biocng_complete_gco2e_mj': e,
                'fuel_saving_fraction_vs_reference': 1-e/reference,
                'biocng_kgco2e_per_leg': qb*e/1000,
                'biocng_kgco2e_total': legs*qb*e/1000,
                'biocng_gco2e_km': qb*e/distance,
                'route_saving_fraction_vs_diesel_energy_reference': 1-qb*e/(qd*reference)} for e in ci_values]}
    central = cases['with_stationary_allowance']['one_leg']
    stress_e = number(ghg['sensitivity_intensity_gco2e_mj'], 'stress intensity')
    stress = []
    for factor in ghg['gas_energy_factors']:
        factor = number(factor, 'gas energy factor', positive=True)
        q = central['biocng_mj']*factor
        stress.append({'gas_energy_factor': factor,
            'route_saving_fraction_vs_diesel_energy_reference': 1-q*stress_e/(central['diesel_mj']*reference),
            'break_even_gco2e_mj': reference*central['diesel_mj']/q})
    canonical = json.dumps(config, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return {'software': 'OLGA Route Model', 'software_version': __version__,
        'input_config_sha256': hashlib.sha256(canonical).hexdigest(),
        'scenario_id': config.get('scenario_id', ''), 'route': route,
        'identical_legs': int(legs), 'profile_results': rows,
        'biocng_properties': fuel, 'cases': cases, 'gas_energy_sensitivity': stress,
        'evidence': config.get('evidence', {}),
        'interpretation': ['Empirical screening calculation; not a dynamic vehicle simulation.',
          'CNG curve is supplied input; aggregate calibration is not reconstructed or validated.',
          'A separately added stationary allowance may double-count effects embedded in a curve.',
          'Bio-CNG assumes unchanged gas-vehicle efficiency and equal fuel-energy demand.',
          'GHG factors must cover the complete declared life-cycle boundary; quality is not sustainability certification.',
          'No concentration-to-g/km conversion, air-pollutant prediction, or statistical confidence interval.']}
