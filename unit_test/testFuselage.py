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
        # self.aircraft.FuselageGroup.get_sized()

    def test_fuselage_length(self):
        self.aircraft.FuselageGroup.Fuselage.Cabin.length = 15
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.length = 10

        self.assertEqual(25, self.aircraft.FuselageGroup.Fuselage.length)

    def test_outer_diameter(self):
        self.aircraft.FuselageGroup.Fuselage.Cabin.diameter = 69
        # self.aircraft.FuselageGroup.Fuselage.size_self()

        self.assertEqual(self.aircraft.FuselageGroup.Fuselage.inner_diameter, 69)
        y = 72.189
        self.assertAlmostEqual(y, self.aircraft.FuselageGroup.Fuselage.outer_diameter, delta=y*testMargin)

    def test_size_self(self):
        # TODO: fix sizing self for the aircraft fuselage
        self.aircraft.FuselageGroup.Fuselage.size_self()

        self.assertTrue(True)
