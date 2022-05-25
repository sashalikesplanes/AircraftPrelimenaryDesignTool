import unittest
from pathlib import Path
from misc.constants import testMargin
from misc.openData import openData
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestWeights(unittest.TestCase):

    def setUp(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"test_state_1": State('test_state_1')}
        self.aircraft = Aircraft(openData(config_file), states)
        # self.aircraft.FuselageGroup.get_sized()

        # Define test params
        self.aircraft.FuselageGroup.Fuselage.Cabin.diameter = 10  # [m]
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.length = 50  # [m]
        self.aircraft.FuselageGroup.Fuselage.Cabin.length = 100         # [m]
        self.aircraft.FuselageGroup.Aircraft.ultimate_load_factor = 2  # [-]
        self.aircraft.FuselageGroup.Aircraft.mtom = 100000  # [kg]
        self.aircraft.FuselageGroup.Fuselage.Cabin.cabin_pressure_altitude = 1000  # [m]
        self.aircraft.WingGroup.Wing.wing_area = 50  # [m2]

    def test_fuselage_mass(self):
        # Test
        self.aircraft.FuselageGroup.Fuselage.size_self()
        x = self.aircraft.FuselageGroup.Fuselage.own_mass
        y = 32452345
        self.assertAlmostEqual(x, y, delta=0.3 * testMargin)


    def test_wing_mass(self):
        # Define params
        pass



    def test_horizontal_tail_mass(self):
        pass

    def test_vertical_tail_mass(self):
        pass

    def test_misc_mass(self):
        pass

