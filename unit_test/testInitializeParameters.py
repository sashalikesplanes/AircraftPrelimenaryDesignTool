import unittest
from misc.constants import testMargin

from conceptualDesign.initializeParameters import initializeParameters

class TestBalloonSizing(unittest.TestCase):
    def testinitialiseParameters(self):
        x = {
            # "altitude": 914,
            "engineEfficiency": 0.6,
            "fuelCellEfficiency": 0.7,

            "wingTaperRatio": 0.8,
            "wingQuarterChordSweep": 20,
            "wingAspectRatio": 8,

            "passengers": 500,
            "cargoMass": 10000,
            "passengerMass": 60000,
            "designConcept": 4


        }  # inputs

        initializeParameters(x)

        #calculated output
        calcwingHalfChordSweep = 1.148119

        # start testing
        self.assertAlmostEqual(calcwingHalfChordSweep, x["wingHalfChordSweep"], delta=calcwingHalfChordSweep * testMargin)