import copy,json,unittest
from pathlib import Path
from olga_route_model.experimental import analyse,describe,normalise_proxy

class ExperimentalTests(unittest.TestCase):
 def setUp(self):self.c=json.loads((Path(__file__).resolve().parents[1]/'examples/experimental_synthetic.json').read_text())
 def test_sample_sd(self):
  r=describe([2,4,6]);self.assertEqual(r['mean'],4);self.assertEqual(r['sample_sd'],2)
 def test_no_missing_value_imputation(self):
  with self.assertRaises(ValueError):describe([1,None,2])
 def test_no_celsius_percentage(self):
  row=analyse(self.c)['stationary_summary'][-1];self.assertIsNone(row['relative_concentration_difference_percent']);self.assertEqual(row['difference_cng_minus_diesel'],-6)
 def test_relative_difference(self):
  row=analyse(self.c)['stationary_summary'][0];self.assertEqual(row['relative_concentration_difference_percent'],-50)
 def test_zero_reference(self):
  for r in self.c['stationary_readings']:
   if r['vehicle']=='Diesel':r['co_ppm']=0
  self.assertIsNone(analyse(self.c)['stationary_summary'][0]['relative_concentration_difference_percent'])
 def test_no_dropped_replicates(self):
  self.c['stationary_readings'].pop()
  with self.assertRaises(ValueError):analyse(self.c)
 def test_reject_duplicate(self):
  self.c['stationary_readings'][1]['rep']=1
  with self.assertRaises(ValueError):analyse(self.c)
 def test_energy_and_mass_units(self):
  r=analyse(self.c);self.assertAlmostEqual(r['speed_segments'][0]['energy_mj_100km'],711.42);self.assertEqual(r['speed_segments'][1]['energy_mj_100km'],500);self.assertEqual(r['cng_route_kg_100km'],20)
 def test_proxy_mass_closure(self):
  r=normalise_proxy([{'relative_rate':2,'duration_s':10},{'relative_rate':4,'duration_s':5}],4)
  self.assertEqual(r['interval_modelled_mass_kg'],[2,2]);self.assertEqual(r['integrated_modelled_mass_kg'],4)
 def test_empty_proxy_rejected(self):
  with self.assertRaises(ValueError):normalise_proxy([],4)

if __name__=='__main__':unittest.main()
