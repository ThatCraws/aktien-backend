import unittest
import util.calculation_helper as CHelper

class CalculationHelperTest(unittest.TestCase):
    
    def test_rsi_list_1(self):
        c = CHelper.calc_rsi([40,220,70,4999])
        self.assertEqual(c,[0.0, 54.54545454545455, 97.14774671990872])
    
    def test_rsi_list_2(self):
        c = CHelper.calc_rsi([50,120,700,5,30])
        self.assertEqual(c,[0.0, 0.0, 48.3271375464684, 49.270072992700726])

    def test_rsi_1(self):
        c = CHelper.calc_current_rsi([300,100,20,6,12,5,20,120,22])
        self.assertAlmostEqual(c,23.26923076923076,3)

    def test_rsi_2(self):
        c = CHelper.calc_current_rsi([30,454,20,2,662])
        self.assertAlmostEqual(c,70.57291666666667,3)

    def test_volatility_1(self):
        c = CHelper.calc_historical_volatility([30,454,20,2,662])
        self.assertAlmostEqual(c*100,273.06380206830784,2)

    def test_volatility_2(self):
        c = CHelper.calc_historical_volatility([23.32,23.22,23.42,22.82,22.22])
        self.assertAlmostEqual(c*100,0.4400,2)


if __name__ =='__main__':
    unittest.main()