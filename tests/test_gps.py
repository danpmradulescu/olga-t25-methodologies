import math
from pathlib import Path
import tempfile
import unittest
from olga_route_model.gps import process_track

ROOT=Path(__file__).resolve().parents[1]
class GPSTests(unittest.TestCase):
    def run_text(self,text,index=None):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'t.kml';p.write_text(text)
            return process_track(p,index)

    def setUp(self):
        self.text=(ROOT/'examples/gps_synthetic.kml').read_text()

    def test_equatorial_arc_and_stationary_interval(self):
        r=self.run_text(self.text)
        self.assertAlmostEqual(r['metrics']['distance_km'],6371*math.pi/180000)
        self.assertEqual(r['metrics']['duration_min'],2)
        self.assertAlmostEqual(r['metrics']['average_speed_kmh'],6371*math.pi/6000)
        self.assertEqual(r['intervals'][1]['speed_kmh'],0)
        self.assertEqual(sum(b['time_percent'] for b in r['speed_bins']),100)

    def test_nonpositive_duration_skipped_without_bridging(self):
        r=self.run_text(self.text.replace('00:01:00Z','00:00:00Z'))
        self.assertEqual(r['skipped_nonpositive_duration_interval_indices'],[0])
        self.assertEqual(r['metrics']['distance_km'],0)
        self.assertTrue(all(b['distance_percent'] is None for b in r['speed_bins']))

    def test_unpaired_and_timezone_free_entries_rejected(self):
        for text in [self.text.replace('<when>2000-01-01T00:02:00Z</when>',''),self.text.replace('Z</when>','</when>')]:
            with self.assertRaises(ValueError):self.run_text(text)

    def test_track_selection_and_xml_rejected(self):
        import re
        track=re.search(r'<gx:Track>.*?</gx:Track>',self.text,re.S).group()
        text=self.text.replace(track,track+track)
        with self.assertRaises(ValueError):self.run_text(text)
        self.assertEqual(self.run_text(text,1)['track_index'],1)
        with self.assertRaises(ValueError):self.run_text('<bad>')

    def test_all_zero_duration_rejected(self):
        text=self.text.replace('00:01:00Z','00:00:00Z').replace('00:02:00Z','00:00:00Z')
        with self.assertRaises(ValueError):self.run_text(text)

if __name__=='__main__':unittest.main()
