import unittest
from pathlib import Path
from misc.constants import testMargin
from misc.openData import openData
from misc.unitConversions import *
from misc.ISA import *
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.FuelCells import FuelCells


class TestWing(unittest.TestCase):
    def setUp(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"test_state_1": State('test_state_1'), "cruise": State("test_state_2")}
        self.aircraft = Aircraft(openData(config_file), states)
        # self.aircraft.FuselageGroup.get_sized()

        # ----- Define test params -----

        # Aircraft
        self.aircraft.FuselageGroup.Aircraft.mtom = 100000  # [kg]
        self.aircraft.reference_area = 50  # [m2]
        self.aircraft.C_D_min = 0.07
        self.aircraft.reference_thrust = 1e6 # [N]

        # Wing
        self.aircraft.WingGroup.Wing.wing_area = 50  # [m2]
        self.aircraft.WingGroup.Wing.span = 20  # [m]
        self.aircraft.WingGroup.Wing.sweep = 0  # [rad]
        self.aircraft.WingGroup.Wing.taper_ratio = 0.8  # [-]
        self.aircraft.WingGroup.Wing.aspect_ratio = 5  # [-]
        self.aircraft.WingGroup.Wing.thickness_chord_ratio = 0.1  # [-]
        self.aircraft.WingGroup.Wing.C_L_0_wing = 0.4  # [-]
        self.aircraft.WingGroup.Wing.C_L_alpha = 0.10966 # [1/deg]

        #Fuselage
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.mass_H2 = 10000 # [kg]

    def test_AR(self):
        model_ARe = self.aircraft.WingGroup.Wing.size_AR()[0]  # [-]
        analytical_ARe = 11.43670084  # [-]
        self.assertAlmostEqual(model_ARe, analytical_ARe, delta = analytical_ARe * testMargin)

    def test_CL_alpha(self):
        model_CL_alpha = self.aircraft.WingGroup.Wing.determine_C_L_alpha()   # [1/deg]
        analytical_CL_alpha =  0.0724558   # [1/deg]
        self.assertAlmostEqual(model_CL_alpha, analytical_CL_alpha, delta = analytical_CL_alpha * testMargin)

    def test_oswald(self):
        model_oswald = self.aircraft.WingGroup.Wing.get_oswald()   # [-]
        analytical_oswald =  0.9007058   # [-]
        self.assertAlmostEqual(model_oswald, analytical_oswald, delta = analytical_oswald * testMargin)

    def test_C_L(self):
     # alpha in [deg]
        model_C_L = self.aircraft.WingGroup.Wing.get_C_L(5)
        analytical_C_L = 0.9483 
        self.assertAlmostEqual(model_C_L, analytical_C_L, delta = analytical_C_L * testMargin)