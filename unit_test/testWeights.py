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

        self.aircraft.WingGroup.Wing.wing_area = 50  # [m2]
        self.aircraft.WingGroup.Wing.span = 20  # [m]
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.own_mass = 50000  # [kg]
        self.aircraft.WingGroup.Wing.sweep = 5  # [deg]
        self.aircraft.WingGroup.Wing.taper_ratio = 0.6  # [-]
        self.aircraft.WingGroup.Wing.aspect_ratio = 5  # [-]
        self.aircraft.WingGroup.Wing.thickness_chord_ratio = 0.1  # [-]


        # Imperial constants from test params:
        # l_FS = 492.12598 # [ft]
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

        analytical_mass_kg = lbs_to_kg(analytical_mass_lbs)

        # analytical_mass_kg = 6443.190189 # test_state_1

        print(f"Mass of fuselage: {model_mass} [kg]")

        self.assertAlmostEqual(model_mass, analytical_mass_kg, delta=analytical_mass_kg * testMargin)

    def test_wing_mass(self):
        # Define params
        self.aircraft.WingGroup.Wing.size_self()
        x =self.aircraft.WingGroup.Wing.own_mass
        y = 1449.007258  # [kg]
        self.assertAlmostEqual(x,y, delta= 0.3* testMargin)

    def test_horizontal_tail_mass(self):
        self.aircraft.FuselageGroup.Tail.HorizontalTail.size_self()
        x = self.aircraft.FuselageGroup.Tail.HorizontalTail.own_mass
        y = 1
        self.assertAlmostEqual(x,y, delta= 0.3* testMargin)


    def test_vertical_tail_mass(self):
        pass

    def test_misc_mass(self):
        print(self.aircraft.FuselageGroup.Fuselage.Cabin.diameter)
        misc = self.aircraft.FuselageGroup.Miscellaneous

        misc.size_self()
        # Boat stuff
        # This y should be the sum of all specified fake fuselage components
        x1 = misc.W_boat
        y1 = 20000
        self.assertAlmostEqual(x1, y1, delta=y1*testMargin)

        # Flight control system
        x2 = misc.W_flight_control_system
        y2 = 32031.317760363490379
        self.assertAlmostEqual(x2, y2, delta=y2 * testMargin)

        # Hydraulics
        x3 = misc.W_hydraulics
        y3 = 99.999999008956208968
        self.assertAlmostEqual(x3, y3, delta=y3 * testMargin)

        # Avionics
        x4 = misc.W_avionics
        # THIS IS STILL A MAGICAL DISNEY NUMBER SO CHANGE WHEN SHIT CHANGES
        W_UAV = 420  # [lbs]
        y4 = (2.117 * W_UAV ** 0.933) * 0.453592
        W_AV = y4 / 0.453592  # [lbs]
        self.assertAlmostEqual(x4, y4, delta=y4 * testMargin)

        # Electrical
        x5 = misc.W_electrical
        # THIS ONCE AGAIN DEPENDS ON THE SAME MAGICAL DISNEY NUMBER
        z5 = (y4 + 50000) * 2.20462
        y5 = 0.453592 * (12.57 * z5 ** 0.51)
        self.assertAlmostEqual(x5, y5, delta=y5 * testMargin)

        # Air Conditioning
        x6 = misc.W_AC
        state6 = State("cruise")
        M = state6.velocity / state6.speed_of_sound
        y6 = (20619.097013151862 * M ** 0.08) * 0.453592
        self.assertAlmostEqual(x6, y6, delta=y6 * testMargin)

        # Furnishing
        x7 = misc.W_furnishing
        y7 = 12765.903532 * 0.453592
        self.assertAlmostEqual(x7, y7, delta=y7 * testMargin)

        x = self.aircraft.FuselageGroup.Miscellaneous.own_mass
        print(f"Mass of miscellaneous group: {x}")
        y = y1 + y2 + y3 + y4 + y5 + y6 + y7
        self.assertAlmostEqual(x, y, delta=y * testMargin)

