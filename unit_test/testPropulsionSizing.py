import unittest
from misc.constants import testMargin

from conceptualDesign.initializeParameters import initializeParameters

class PropSizing(unittest.TestCase):
    def testPropulsionSizing(self):
        x = {
            "totalDrag": 1,
            "velocity": 1,
            "engineEfficiency": 1,
            "fuelCellEfficiency": 1,
            "engineSpecificPower": 1,
            "fuelCellSpecificPower": 1
        }
    propulsionsizing(x)

    # calculated output
     = 0.487474

    # start testing
    self.assertAlmostEqual(calcwingHalfChordSweep, x["wingHalfChordSweep"], delta=calcwingHalfChordSweep * testMargin)