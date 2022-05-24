import unittest
from pathlib import Path

from misc.constants import testMargin
from misc.openData import openData
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestWeights(unittest.TestCase):
    # def __init__(self):
    #     states_dict = {"cruise": State("cruise")}
    #
    #     config_file = Path('data', 'new_designs', 'config.yaml')
    #     self.aircraft = Aircraft(openData(config_file), states_dict)

    def test_fuselage_weight(self):
        states_dict = {"cruise": State("cruise")}
        config_file = Path('data', 'new_designs', 'config.yaml')
        aircraft = Aircraft(openData(config_file), states_dict)

        aircraft.get_sized()
        print(aircraft.FuselageGroup.Fuselage.own_mass)

        self.assertAlmostEqual(0.1+0.2, 0.3, delta=0)

    def test_wing_weight(self):
        pass
