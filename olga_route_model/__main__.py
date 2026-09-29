import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

from . import __version__
from .model import calculate, kml_route


def main():
    parser = argparse.ArgumentParser(description='OLGA route fuel and conditional life-cycle GHG screening model')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--input', type=Path, required=True, help='Scenario JSON')
    parser.add_argument('--output', type=Path, required=True, help='Output directory; existing results must be removed explicitly')
    parser.add_argument('--kml', type=Path, help='Optional KML to replace the scenario distance')
    parser.add_argument('--line-index', type=int, help='Zero-based LineString selection')
    args = parser.parse_args()
    try:
        if args.line_index is not None and args.kml is None:
            raise ValueError('--line-index requires --kml')
        cfg = json.loads(args.input.read_text(encoding='utf-8'))
        route = kml_route(args.kml, args.line_index, cfg['route'].get('earth_radius_km', 6371.0)) if args.kml else None
        result = calculate(cfg, route)
        result['execution'] = {'python_version': sys.version.split()[0],
            'input_file_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
            'model_source_sha256': hashlib.sha256(Path(__file__).with_name('model.py').read_bytes()).hexdigest()}
        args.output.mkdir(parents=True, exist_ok=True)
        targets = [args.output/n for n in ('results.json', 'profile.csv', 'summary.csv')]
        if any(p.exists() for p in targets):
            raise ValueError('Output files already exist; choose a new directory')
        targets[0].write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
        with targets[1].open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(result['profile_results'][0]))
            writer.writeheader(); writer.writerows(result['profile_results'])
        with targets[2].open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f); writer.writerow(['case','metric','one_leg','identical_legs_total'])
            for name, case in result['cases'].items():
                for metric, value in case['one_leg'].items():
                    writer.writerow([name, metric, value, case['identical_legs_total'][metric]])
        print(f"OLGA Route Model {__version__}: results saved to {args.output}")
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f'Input/output error: {exc}\n')


if __name__ == '__main__':
    main()
