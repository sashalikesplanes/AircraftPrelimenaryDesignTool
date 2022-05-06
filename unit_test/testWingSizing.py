import unittest
from misc.constants import testMargin

from conceptualDesign.wingSizing import wingSizing

class TestWingSizing(unittest.TestCase):
    def testWingSizing(self):
        x = {
            "designConcept": 3,
            "totalMass": 60000,
            "balloonLift": 500000,
            "liftFactor": 5,
            "velocity": 80,   #m/s
            "wingC_L_design": 1,
            'wingDragCorrection': 1,
            "wingC_D_0": 0.02,
            "wingAspectRatio": 8,
            "wingHalfChordSweep": 0.5,
            "thicknessOverChord": 1,
            "maxLoadFactor": 5


        }  # inputs

        rho = 1.225

        wingSizing(x,rho)


        #calculated output
        calcwingStrMass = 1778.592959

        # start testing
        self.assertAlmostEqual(calcwingStrMass, x["wingStructuralMass"], delta=calcwingStrMass * testMargin)