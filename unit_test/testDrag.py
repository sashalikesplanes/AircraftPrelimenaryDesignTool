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


class TestDrag(unittest.TestCase):
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
        T = 178.84

        x = calc_viscosity(T)
        y = 1.206e-5
        self.assertAlmostEqual(x, y, delta=y * testMargin)

    def test_reynolds(self):
        T = 178.84
        rho = 1
        V = 100
        c = 3

        x = calc_reynolds(rho, V, c, T)
        y = 24.9e6
        self.assertAlmostEqual(x, y, delta=y * testMargin)

        V_2 = 500
        x_2 = calc_reynolds(rho, V_2, c, T) 
        y_2 = 36.14e6
        self.assertAlmostEqual(x_2, y_2, delta=y * testMargin)


    def test_Cf(self):
        Re = 24.0e9
        Xtroverc = 0.15
        x = calc_Cf(Re, Xtroverc)
        y = 54.6e-5
        self.assertAlmostEqual(x, y, delta=y * testMargin)


    def test_CDfwing(self):
        dfus = 10
        croot = 10
        toverc = 0.15
        Sref = 2000
        Cf = 54.6e-5

        x = calc_CDfwing(dfus, croot, toverc, Sref, Cf)
        y = 1.07e-3
        self.assertAlmostEqual(x, y, delta=y * testMargin)




    def test_CDffus(self):
        dfus = 10
        cfus = 100
        Sref = 2000
        Cf = 54.6e-5

        x = calc_CDffus(Sref, cfus, dfus, Cf)
        y = 9.28e-4
        self.assertAlmostEqual(x, y, delta=y * testMargin)

    def test_CDftail(self):
        toverc = 0.15
        Stail = 500
        Sref = 2000
        Cf = 54.6e-5

        x = calc_CDftail(toverc, Stail, Sref, Cf)
        y = 2.81e-4
        self.assertAlmostEqual(x, y, delta=y * testMargin)

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
