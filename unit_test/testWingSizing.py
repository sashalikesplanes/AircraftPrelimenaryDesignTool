import unittest
from misc.constants import testMargin

from conceptualDesign.wingSizing import wingSizing

class TestWingSizing(unittest.TestCase):
    def testWingSizing(self):
        x = {
            "designConcept": 1,
            "totalMass": 800000,
            "balloonLift": 1,
            "liftFactor": 1.1,
            "velocity": 80,   #m/s
            "wingC_L_design": 1,
            'wingDragCorrection': 1,
            "wingC_D_0": 0.2,
            "wingAspectRatio": 8,
            "wingHalfChordSweep": 0.5,
            "thicknessOverChord": 0.3,
            "maxLoadFactor": 3


        }  # inputs

        rho = 1.225

        wingSizing(x,rho)


        #calculated output
        calcwingStrMass = 43345363.12

        # start testing
        self.assertAlmostEqual(calcwingStrMass, x["wingStructuralMass"], delta=calcwingStrMass * testMargin)