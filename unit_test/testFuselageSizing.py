import unittest
from misc.constants import testMargin

from conceptualDesign.fuselageSizing import fuselageWeight, fuselageSizing


class TestFuselageSizing(unittest.TestCase):
    def test_fuselage_sizing(self):
        # dictionary with all required inputs
        x = {
            "passengers": 200,
            "cargoMass": 10000,
            "passengerMass": 100
        }
        fuselageSizing(x)

        self.assertAlmostEqual(33.93, x["cabinLength"], delta=33.93*testMargin)
        self.assertAlmostEqual(5.079, x["fuselageDiameter"], delta=5.079*testMargin)
        self.assertAlmostEqual(21288.59919, x["fuselageStructuralMass"], delta=21288.59919*testMargin)

    def test_fuselage_weight(self):
        x = {
            "totalMass": 25000,
            "cabinLength": 37,
            "fuselageDiameter": 4,
            "wingQuarterChordSweep": 0.2,
            "wingAspectRatio": 7,
            "wingArea": 21,
            "wingTaperRatio": 0.5,
            "kws": 0
        }
        # This function is fairly nasty since it uses lots of retard units
        fuselageWeight(x)

        self.assertAlmostEqual(0.3114469781034549, x['kws'], delta=0.3114469781034549*testMargin)
