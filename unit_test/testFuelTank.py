import unittest
from pathlib import Path
from misc.constants import testMargin
from misc.openData import openData
from misc.unitConversions import *
from misc.ISA import *
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestWeights(unittest.TestCase):

    def setUp(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"test_state_1": State('test_state_1'), "cruise": State("test_state_2")}
        self.aircraft = Aircraft(openData(config_file), states)
        # self.aircraft.FuselageGroup.get_sized()

        # Define test params
        self.aircraft.FuselageGroup.Fuselage.Cabin.diameter = 10  # [m]
        self.aircraft.FuselageGroup.Fuselage.Cabin.length = 100  # [m]
        self.aircraft.FuselageGroup.Fuselage.Cabin.cabin_pressure_altitude = 2000  # [m]
        self.aircraft.FuselageGroup.Fuselage.Cabin.passengers = 250  # [-]

        self.aircraft.FuselageGroup.Fuselage.FuelContainer.length = 50  # [m]

        self.aircraft.FuselageGroup.Aircraft.ultimate_load_factor = 2  # [-]
        self.aircraft.FuselageGroup.Aircraft.mtom = 100000  # [kg]
        self.aircraft.FuselageGroup.Fuselage.own_mass = 50000  # [kg]
        self.aircraft.reference_area = 50

        self.aircraft.WingGroup.Wing.wing_area = 50  # [m2]
        self.aircraft.WingGroup.Wing.span = 20  # [m]
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.own_mass = 50000  # [kg]
        self.aircraft.WingGroup.Wing.sweep = 5  # [deg]
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

    def test_fuselage_mass(self):
        self.aircraft.FuselageGroup.Fuselage.size_self()
        state = self.aircraft.FuselageGroup.Aircraft.states["cruise"]

        # mass test
        model_mass = self.aircraft.FuselageGroup.Fuselage.own_mass

        # Adapting values for changing cruise state
        q = pa_to_psf(0.5 * state.density * state.velocity ** 2)  # [psi]
        Delta_P = pa_to_psi(
            getPressure(self.aircraft.FuselageGroup.Fuselage.Cabin.cabin_pressure_altitude) - state.pressure)  # [psi]
        if Delta_P < 0:
            Delta_P = 0

        analytical_mass_lbs = 0.052 * 55308.51562 ** 1.086 * 440924.5244 ** 0.177 * 270.74245 ** -0.051 * (
                492.12598 / 32.8084) ** (
                                  -0.072) * q ** 0.241 + 11.9 * (277360.9475 * Delta_P) ** 0.271

        analytical_mass_kg = lbs_to_kg(analytical_mass_lbs)     # cruise state

        # analytical_mass_kg = 6443.190189 # test_state_1

        self.assertAlmostEqual(model_mass, analytical_mass_kg, delta=analytical_mass_kg * testMargin)