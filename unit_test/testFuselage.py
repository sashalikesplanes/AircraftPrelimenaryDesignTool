import unittest
from pathlib import Path

from misc.constants import testMargin
from misc.openData import openData
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestFuselage(unittest.TestCase):
    def setUp(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"cruise": State('cruise')}
        self.aircraft = Aircraft(openData(config_file), states)
        self.aircraft.FuselageGroup.get_sized()

    def test_fuselage_mass(self):
        print(self.aircraft)