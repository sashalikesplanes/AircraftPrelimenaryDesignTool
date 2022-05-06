import unittest
from misc.constants import testMargin

from conceptualDesign.balloonSizing import balloonSizing


class TestBalloonSizing(unittest.TestCase):
    def test1(self):
        x = {
            "designConcept": 2,
            "fuelMass": 5000,
            "compressionRatio": 2,
            "liftingHydrogenMass": 5000,
            "balloonFinesseRatio": 10,
            "factorOfSafety": 1,
            "containerToFuelMassRatio": 0.4
        }  # inputs
        y = 0  # calculated result

        # Other things the functions takes
        rho = 1
        p = 100000
        balloonSizing(x, rho, p)

        self.assertAlmostEqual(y, x["balloonStructuralMass"], delta=y * testMargin)


