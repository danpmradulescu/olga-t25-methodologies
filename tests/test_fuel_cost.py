import copy
import json
from pathlib import Path
import unittest
from olga_route_model.fuel_cost import calculate_costs

class CostTests(unittest.TestCase):
    def setUp(self):
        self.cfg=json.loads((Path(__file__).resolve().parents[1]/'examples/fuel_cost_synthetic.json').read_text())

    def test_hand_calculated_costs_and_thresholds(self):
        rows=calculate_costs(self.cfg)['fuel_costs']
        self.assertEqual(rows[0]['route_cost'],48)
        self.assertEqual(rows[1]['route_cost'],36)
        self.assertEqual(rows[1]['cost_per_km'],1.8)
        self.assertEqual(rows[1]['difference_vs_diesel_percent'],-25)
        self.assertEqual(rows[1]['price_for_equal_diesel_fuel_cost'],12)
        self.assertAlmostEqual(rows[2]['price_for_equal_diesel_fuel_cost'],120/11)

    def test_equal_expenditure_at_break_even(self):
        self.cfg['fuels']['CNG']['unit_price']=12
        self.assertEqual(calculate_costs(self.cfg)['fuel_costs'][1]['difference_vs_diesel_percent'],0)

    def test_sensitivity_is_product_and_diesel_fixed(self):
        self.cfg['consumption_factors']=[1.25];self.cfg['price_factors']=[2]
        result=calculate_costs(self.cfg)
        self.assertEqual(result['sensitivity'][0]['route_cost'],90)
        self.assertEqual(result['sensitivity'][0]['difference_vs_fixed_diesel_percent'],87.5)
        self.assertEqual(result['fuel_costs'][0]['route_cost'],48)

    def test_incompatible_units_and_taxes_rejected(self):
        for field,value in [('quantity_unit','L'),('price_unit','EUR/kg'),('price_basis','VAT_exclusive')]:
            c=copy.deepcopy(self.cfg);c['fuels']['CNG'][field]=value
            with self.assertRaises(ValueError):calculate_costs(c)

    def test_invalid_denominators_and_missing_sources(self):
        for val in [0,-1,float('nan'),True]:
            c=copy.deepcopy(self.cfg);c['distance_km']=val
            with self.assertRaises(ValueError):calculate_costs(c)
        self.cfg['fuels']['CNG']['price_source']=''
        with self.assertRaises(ValueError):calculate_costs(self.cfg)

    def test_empty_sensitivity_rejected(self):
        self.cfg['consumption_factors']=[]
        with self.assertRaises(ValueError):calculate_costs(self.cfg)

if __name__=='__main__':unittest.main()
