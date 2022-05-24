import unittest
from pathlib import Path
from misc.constants import testMargin
from misc.openData import openData
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestWeights(unittest.TestCase):

    def setUp(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"stationary": State('stationary')}
        self.aircraft = Aircraft(openData(config_file), states)
        # self.aircraft.FuselageGroup.get_sized()

    def test_fuselage_mass(self):
        # Define params
        self.aircraft.FuselageGroup.Fuselage.Cabin.diameter = 10    # [m]
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.length = 50    # [m]
        self.aircraft.FuselageGroup.Fuselage.Cabin.length = 100
        self.aircraft.FuselageGroup.Aircraft.ultimate_load_factor = 2    # [-]
        self.aircraft.FuselageGroup.Aircraft.mtom = 100000  # [kg]
        self.aircraft.FuselageGroup.Fuselage.Cabin.cabin_pressure_altitude = 1000   # [m]

        # Test
        self.aircraft.FuselageGroup.Fuselage.size_self()
        x = self.aircraft.FuselageGroup.Fuselage.own_mass
        y = 32452345
        self.assertAlmostEqual(x, y, delta=0.3 * testMargin)


    def test_wing_mass(self):
        # Define params
        self.aircraft.WingGroup.Wing.wing_area = 50



    def test_horizontal_tail_mass(self):
        pass

    def test_vertical_tail_mass(self):
        pass

    def test_misc_mass(self):
        pass

