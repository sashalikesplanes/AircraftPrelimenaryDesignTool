import unittest
from pathlib import Path

from misc.constants import testMargin
from misc.openData import openData
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestSizing(unittest.TestCase):
    def test_fuselage_group_sizing(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"cruise": State('cruise')}
        aircraft = Aircraft(openData(config_file), states)
        aircraft.FuselageGroup.get_sized()

        self.assertAlmostEqual(0.3, 0.2 + 0.1, delta=0.3 * testMargin)

    def test_wing_group_sizing(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"cruise": State('cruise')}
        aircraft = Aircraft(openData(config_file), states)
        aircraft.WingGroup.get_sized()

        self.assertAlmostEqual(0.3, 0.2 + 0.1, delta=0.3 * testMargin)
