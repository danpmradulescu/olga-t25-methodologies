"""Timestamped gx:Track processing, separate from geometry-only route screening."""
import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from . import __version__
from .model import haversine_km, number


def process_track(path, track_index=None):
    data = Path(path).read_bytes()
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('XML document types and entities are unsupported')
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError('Invalid KML') from exc
    ns = {'k':'http://www.opengis.net/kml/2.2','gx':'http://www.google.com/kml/ext/2.2'}
    tracks = list(root.findall('.//gx:Track',ns))
    if not tracks:
        raise ValueError('No gx:Track present; a LineString alone has no timed speed profile')
    if track_index is None:
        if len(tracks) != 1:
            raise ValueError('Select one track explicitly; tracks are never joined automatically')
        track_index = 0
    if not 0 <= track_index < len(tracks):
        raise ValueError('Track index out of range')
    track = tracks[track_index]
    times = [datetime.fromisoformat((e.text or '').replace('Z','+00:00')) for e in track.findall('k:when',ns)]
    if any(t.tzinfo is None for t in times):
        raise ValueError('Explicit timestamp timezone required')
    coords = [tuple(map(float,(e.text or '').split())) for e in track.findall('gx:coord',ns)]
    if len(times) != len(coords) or len(times) < 2:
        raise ValueError('At least two paired coordinates/timestamps required; unmatched entries are not truncated')
    for point in coords:
        if len(point) != 3:
            raise ValueError('Expected longitude latitude altitude')
        haversine_km(point[:2],point[:2])
        number(point[2],'altitude')
    rows = []; skipped = []
    for i in range(len(times)-1):
        dt = (times[i+1]-times[i]).total_seconds()
        if dt <= 0:
            skipped.append(i)
            continue
        distance = haversine_km(coords[i][:2],coords[i+1][:2])*1000
        rows.append({'interval_index':i,'elapsed_s':(times[i]-times[0]).total_seconds(),
                     'duration_s':dt,'distance_m':distance,'speed_kmh':3.6*distance/dt})
    if not rows:
        raise ValueError('No positive-duration intervals')
    total_d = math.fsum(r['distance_m'] for r in rows)
    total_t = math.fsum(r['duration_s'] for r in rows)
    metrics = {'points':len(coords),'distance_km':total_d/1000,'duration_min':total_t/60,
               'average_speed_kmh':3.6*total_d/total_t,
               'maximum_speed_kmh':max(r['speed_kmh'] for r in rows),
               'altitude_min_m':min(c[2] for c in coords),'altitude_max_m':max(c[2] for c in coords)}
    bins = []
    for low in range(0,61,10):
        high = low+10 if low < 60 else math.inf
        subset = [r for r in rows if low <= r['speed_kmh'] < high]
        bins.append({'bin_kmh':f'[{low},{low+10})' if low < 60 else '[60,infinity)',
            'time_percent':100*math.fsum(r['duration_s'] for r in subset)/total_t,
            'distance_percent':100*math.fsum(r['distance_m'] for r in subset)/total_d if total_d else None})
    return {'software':'OLGA Route Model','version':__version__,'module':'gps',
        'input_sha256':hashlib.sha256(data).hexdigest(),'track_index':track_index,
        'earth_radius_km':6371.0,'metrics':metrics,'speed_bins':bins,'intervals':rows,
        'skipped_nonpositive_duration_interval_indices':skipped,
        'interpretation':['Horizontal spherical distances; elevation is not used for slope corrections.',
            'No smoothing or outlier filtering. Interval speed is not an instantaneous sensor speed.',
            'Nonpositive-duration intervals are excluded and reported, without bridging gaps.',
            'Accepted-interval duration need not equal elapsed wall-clock duration.',
            'Zero distance yields undefined distance shares, represented by null.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--track-index',type=int)
    a = p.parse_args()
    try:
        result = process_track(a.input,a.track_index)
        result['execution'] = {'python_version':sys.version.split()[0],
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        files = [a.output/n for n in ('gps_results.json','gps_intervals.csv','gps_speed_bins.csv')]
        if any(f.exists() for f in files):
            raise ValueError('Outputs already exist; choose a new directory')
        a.output.mkdir(parents=True,exist_ok=True)
        files[0].write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        for path,rows in zip(files[1:],(result['intervals'],result['speed_bins'])):
            with path.open('w',newline='',encoding='utf-8') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
        print(f'GPS results saved to {a.output}')
    except (ValueError,KeyError,TypeError,OSError) as exc:
        p.exit(2,f'Input/output error: {exc}\n')


if __name__ == '__main__':
    main()
