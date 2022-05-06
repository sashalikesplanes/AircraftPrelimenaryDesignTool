import unittest
from misc.constants import testMargin

from conceptualDesign.initializeParameters import initializeParameters

class InitializeParameters(unittest.TestCase):
    def testinitialiseParameters(self):
        x = {
            # "altitude": 914,
            "engineEfficiency": 0.6,
            "fuelCellEfficiency": 0.7,

            "wingTaperRatio": 0.8,
            "wingQuarterChordSweep": 0.5,
            "wingAspectRatio": 5,

            "passengers": 500,
            "cargoMass": 10000,
            "passengerMass": 60000,
            "designConcept": 4


        }  # inputs

        initializeParameters(x)

        #calculated output
        calcwingHalfChordSweep = 0.487474

        # start testing
        self.assertAlmostEqual(calcwingHalfChordSweep, x["wingHalfChordSweep"], delta=calcwingHalfChordSweep * testMargin)