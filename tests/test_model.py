import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
from olga_route_model.model import calculate, haversine_km, interpolate, kml_route, mixture_properties

ROOT = Path(__file__).resolve().parents[1]

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((ROOT/'examples/synthetic.json').read_text())
        self.cfg['distance_profile'] = [{'speed_kmh':30,'distance_fraction':1}]
        self.cfg['diesel']['curve'] = [[10,20],[50,20]]
        self.cfg['cng']['curve'] = [[10,10],[50,10]]
        self.cfg['biocng']['dry_mole_fractions'] = {'CH4':1,'CO2':0,'N2':0}

    def test_hand_calculated_fuel_time_and_idle(self):
        r=calculate(self.cfg)['cases']
        self.assertAlmostEqual(r['movement_only']['one_leg']['diesel_l'],2)
        self.assertAlmostEqual(r['movement_only']['one_leg']['cng_kg'],1)
        self.assertAlmostEqual(r['movement_only']['one_leg']['duration_min'],20)
        self.assertAlmostEqual(r['with_stationary_allowance']['one_leg']['diesel_l'],2.2)
        self.assertAlmostEqual(r['with_stationary_allowance']['one_leg']['cng_kg'],1.2)
        self.assertAlmostEqual(r['with_stationary_allowance']['one_leg']['duration_min'],26)
        self.assertAlmostEqual(r['with_stationary_allowance']['identical_legs_total']['diesel_l'],4.4)

    def test_equal_energy_pure_methane(self):
        r=calculate(self.cfg)['cases']['with_stationary_allowance']['one_leg']
        self.assertAlmostEqual(r['biocng_kg'],r['cng_kg'])
        self.assertAlmostEqual(r['biocng_mj'],60)

    def test_energy_and_ghg_are_distinct(self):
        r=calculate(self.cfg)['cases']['with_stationary_allowance']
        qd=2.2*.835*42.6
        self.assertAlmostEqual(r['one_leg']['diesel_mj'],qd)
        scenario=r['ghg']['scenarios'][1]
        self.assertAlmostEqual(scenario['fuel_saving_fraction_vs_reference'],.7)
        self.assertAlmostEqual(scenario['route_saving_fraction_vs_diesel_energy_reference'],1-60*28.2/(qd*94))
        self.assertAlmostEqual(r['ghg']['biocng_break_even_gco2e_mj'],94*qd/60)

    def test_mixture_mass_not_mole_fraction(self):
        m=mixture_properties({'dry_mole_fractions':{'CH4':.97,'CO2':.02,'N2':.01},'methane_lhv_mj_kg':50})
        self.assertAlmostEqual(m['molar_mass_kg_kmol'],16.72205)
        self.assertAlmostEqual(m['lhv_mj_kg'],46.53050911820022)
        self.assertLess(m['methane_mass_fraction'],.97)

    def test_interpolation_and_exact_nodes(self):
        self.assertEqual(interpolate([[10,40],[30,20]],15),35)
        self.assertEqual(interpolate([[10,40],[30,20]],30),20)

    def test_reject_extrapolation_and_duplicate_nodes(self):
        for curve,v in [([[10,40],[30,20]],5),([[10,40],[10,20]],10)]:
            with self.assertRaises(ValueError): interpolate(curve,v)

    def test_reject_invalid_inputs(self):
        for field,value in [('minutes_per_leg',-1),('cng_kg_h',float('nan'))]:
            c=copy.deepcopy(self.cfg);c['stationary_allowance'][field]=value
            with self.assertRaises(ValueError): calculate(c)
        self.cfg['distance_profile'][0]['distance_fraction']=.9
        with self.assertRaises(ValueError): calculate(self.cfg)

    def test_haversine_known_arc(self):
        self.assertAlmostEqual(haversine_km((0,0),(90,0)),6371*math.pi/2)
        self.assertEqual(haversine_km((23,46),(23,46)),0)

    def test_kml_selection_and_bad_xml(self):
        line='<LineString><coordinates>0,0,0 90,0,0</coordinates></LineString>'
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'route.kml';p.write_text('<kml>'+line+line+'</kml>')
            with self.assertRaises(ValueError): kml_route(p)
            self.assertAlmostEqual(kml_route(p,1)['one_way_distance_km'],6371*math.pi/2)
            p.write_text('<broken>')
            with self.assertRaises(ValueError): kml_route(p)

    def test_sensitivity_direction(self):
        r=calculate(self.cfg)['gas_energy_sensitivity']
        self.assertGreater(r[0]['route_saving_fraction_vs_diesel_energy_reference'],r[2]['route_saving_fraction_vs_diesel_energy_reference'])

if __name__ == '__main__': unittest.main()
