import unittest
from misc.constants import testMargin

from conceptualDesign.balloonSizing import balloonSizing


class TestBalloonSizing(unittest.TestCase):
    # def test1(self):
    #     x = {
    #         "designConcept": 3,
    #         "fuelMass": 5000,
    #         "compressionRatio": 700,
    #         "liftingHydrogenMass": 7.153,
    #         "balloonFinesseRatio": 100,
    #         "factorOfSafety": 1,
    #         "containerToFuelMassRatio": 0.4
    #     }  # inputs
    #     calcStrMass = 79935 # calculated result
    #     calcSurfArea = 341
    #
    #     # Other things the functions takes
    #     rhoAir = 0.225
    #     p = 100000
    #     balloonSizing(x, rhoAir, p)
    #
    #     self.assertAlmostEqual(calcStrMass, x["balloonStructuralMass"], delta=calcStrMass * testMargin)
    #     self.assertAlmostEqual(calcSurfArea, x["balloonSurfaceArea"], delta=calcSurfArea * testMargin)



    def test2(self):
        x = {
            "designConcept": 4,
            "fuelMass": 5000,
            "compressionRatio": 20,
            "liftingHydrogenMass": 263.1579,
            "balloonFinesseRatio": 100,
            "factorOfSafety": 1,
            "containerToFuelMassRatio": 2

        }  # inputs
        calcStrMass = 10000 # calculated result
        # calcSurfArea = 341
        calcLength = 12.679

        # Other things the functions takes
        rhoAir = 0.225
        p = 100000
        balloonSizing(x, rhoAir, p)



        self.assertAlmostEqual(calcStrMass, x["balloonStructuralMass"], delta=calcStrMass * testMargin)
        # self.assertAlmostEqual(calcSurfArea, x["balloonSurfaceArea"], delta=calcSurfArea * testMargin)
        self.assertAlmostEqual(calcLength, x["balloonLength"], delta=calcLength * testMargin)

