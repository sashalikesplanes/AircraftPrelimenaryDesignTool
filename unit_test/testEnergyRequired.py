import unittest
from misc.constants import testMargin

from conceptualDesign.energyRequired import energyRequired


class TestEnergyRequired(unittest.TestCase):
    def test_solar_absence(self):
        x = {
            "totalDrag": 2,
            "flightRange": 3,
            "velocity": 5,
            "propEfficiency": 0.7,
            "hasSolarPanels": False,

            "balloonLength": 11,
            "balloonRadius": 13
        }
        energyRequired(x)

        # Assert the values in the params to the expected results
        self.assertAlmostEqual(8.5714286, x["requiredEnergy"], delta=8.5714286*testMargin)
        # Assert if there are no solar panels when we disable solar panels
        self.assertEqual(0, x["solarPower"])
        self.assertEqual(0, x["solarMass"])
        self.assertEqual(0, x["solarEnergy"])

    def test_solar(self):
        x = {
            "totalDrag": 2,
            "flightRange": 3,
            "velocity": 5,
            "propEfficiency": 0.7,
            "hasSolarPanels": True,

            "balloonLength": 11,
            "balloonRadius": 13
        }
        energyRequired(x)

        # Assert the values in the params to the expected results
        self.assertAlmostEqual(8.5714286, x["requiredEnergy"], delta=8.5714286*testMargin)
        # Assert if there are no solar panels when we disable solar panels
        self.assertAlmostEqual(45833.333, x["solarPower"], delta=45833.333 * testMargin)
        self.assertAlmostEqual(654.7619, x["solarMass"], delta=654.7619 * testMargin)
        self.assertAlmostEqual(27500, x["solarEnergy"], delta=27500 * testMargin)
