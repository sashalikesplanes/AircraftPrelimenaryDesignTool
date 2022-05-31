import unittest
from pathlib import Path
from misc.constants import testMargin
from misc.openData import openData
from misc.unitConversions import *
from misc.ISA import *
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.FuelCells import FuelCells
from detailedDesign.get_drag import *


class TestFuelTank(unittest.TestCase):
    def setUp(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"test_state_1": State('test_state_1'), "cruise": State("test_state_2")}
        self.aircraft = Aircraft(openData(config_file), states)
        # self.aircraft.FuselageGroup.get_sized()

        # ----- Define test params -----
        self.aircraft.FuselageGroup.Power.own_power_peak = 100e6
        self.aircraft.FuselageGroup.Power.own_power_average = 50e6

        self.aircraft.FuselageGroup.Power.FuelCells.mass_power_density = 10000
        self.aircraft.FuselageGroup.Power.FuelCells.W_Size = 1000

        # Fuel tank
        self.aircraft.FuselageGroup.Fuselage.Cabin.diameter = 10

        # Fuselage
        self.aircraft.FuselageGroup.Fuselage.Cabin.diameter = 10  # [m]
        self.aircraft.FuselageGroup.Fuselage.Cabin.length = 100  # [m]
        self.aircraft.FuselageGroup.Fuselage.Cabin.cabin_pressure_altitude = 2000  # [m]
        self.aircraft.FuselageGroup.Fuselage.Cabin.passengers = 250  # [-]

        self.aircraft.FuselageGroup.Fuselage.FuelContainer.length = 50  # [m]

        # Aircraft
        self.aircraft.FuselageGroup.Aircraft.ultimate_load_factor = 2  # [-]
        self.aircraft.FuselageGroup.Aircraft.mtom = 100000  # [kg]
        self.aircraft.FuselageGroup.Fuselage.own_mass = 50000  # [kg]
        self.aircraft.reference_area = 50

        # Wing
        self.aircraft.WingGroup.Wing.wing_area = 50  # [m2]
        self.aircraft.WingGroup.Wing.span = 20  # [m]
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.own_mass = 50000  # [kg]
        self.aircraft.WingGroup.Wing.sweep = 0.0872665  # [rad]
        self.aircraft.WingGroup.Wing.taper_ratio = 0.6  # [-]
        self.aircraft.WingGroup.Wing.aspect_ratio = 5  # [-]
        self.aircraft.WingGroup.Wing.thickness_chord_ratio = 0.1  # [-]

        # Imperial constants from test params:
        # l_FS = 492.12598    # [ft]
        # S_fus = 55308.51562 # [ft2]
        # W_o = 220462.2622   # [lbs]
        # l_HT = 270.74245    # [ft]
        # d_FS = 32.8084      # [ft]
        # q = 0.0080615       # [psi] for test_state_1
        # V_p = 277360.9475   # [ft3] for test_state_1
        # Delta_P = 0         # [psi] for test_state_1

    def test_viscosity(self):
        T = 10

        x = calc_viscosity(T)
        y = 43245
        self.assertAlmostEqual(x, y, delta=y * testMargin)

    def test_reynolds(self):
        pass

    def test_Cf(self):
        pass

    def test_CDfwing(self):
        pass

    def test_CDffus(self):
        pass

    def test_CDftail(self):
        pass

    def test_FFwing(self):
        pass

    def test_FFfuselage(self):
        pass

    def test_FFnacele(self):
        pass

    def test_CDmin_wing(self):
        pass

    def test_CDmin_fuselage(self):
        pass

    def test_CDmin_tail(self):
        pass

    def test_CDmin(self):
        pass

    def test_CDi(self):
        pass

    def test_get_drag(self):
        pass
