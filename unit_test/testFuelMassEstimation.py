import unittest
from misc.constants import testMargin

from conceptualDesign.fuelMassEstimation import fuelMassEstimation


class TestFuelMassEstimation(unittest.TestCase):
    def test1(self):
        x = {
            "requiredEnergy": 30e6,
            "solarEnergy": 50e6,
        }
        fuelMassEstimation(x)

        self.assertAlmostEqual(-0.16534391534391535, x["fuelMass"], delta=abs(-0.16534391534391535*testMargin))

    def test2(self):
        x = {
            "requiredEnergy": 1e9,
            "solarEnergy": 0,
        }
        fuelMassEstimation(x)

        self.assertAlmostEqual(8.267195767195767, x["fuelMass"], delta=abs(8.267195767195767*testMargin))