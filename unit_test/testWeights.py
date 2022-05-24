import unittest
from pathlib import Path

from misc.constants import testMargin
from misc.openData import openData
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestWeights(unittest.TestCase):
    def test_upper(self):
        self.assertAlmostEqual(0.3, 0.2+0.1, delta=0.3*testMargin)

        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"cruise": State('cruise')}
        aircraft = Aircraft(openData(config_file), states)
        aircraft.get_sized()

        fuselage_weight = aircraft.FuselageGroup.Fuselage.get_mass()
        print(fuselage_weight)
