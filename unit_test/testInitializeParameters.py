import unittest
from misc.constants import testMargin

from conceptualDesign.initializeParameters import initializeParameters

class TestBalloonSizing(unittest.TestCase):
    def testinitialiseParameters(self):
        x = {
            "altitude": 1
            "engineEfficiency": 1
            "fuelCellEfficiency": 1
            "wingTaperRatio": 1
            "wingQuarterChordSweep": 1
            "wingAspectRatio": 1

        }  # inputs

        initializeParameters(x)

        #calculated output
        wingHalfChordSweep = 1

        # start testing
        self.assertAlmostEqual(wingHalfChordSweep, x["wingHalfChordSweep"], delta=wingHalfChordSweep * testMargin)