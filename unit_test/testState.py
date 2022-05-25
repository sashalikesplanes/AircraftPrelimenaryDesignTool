import unittest

from misc.constants import testMargin
from detailedDesign.classes.State import State


class TestState(unittest.TestCase):
    def test_stationary_state(self):
        self.state = State("test_state_1")

        self.assertEqual(self.state.velocity, 10)
        self.assertEqual(self.state.altitude, 1000)
        self.assertEqual(self.state.range, 100000)

        y = 89874.6
        self.assertAlmostEqual(self.state.pressure, y, delta=y*testMargin)
        y = 281.650
        self.assertAlmostEqual(self.state.temperature, y, delta=y*testMargin)
        y = 1.11164
        self.assertAlmostEqual(self.state.density, y, delta=y*testMargin)
        y = 336.434
        self.assertAlmostEqual(self.state.speed_of_sound, y, delta=y*testMargin)

    def test_high_place_state(self):
        self.state = State("test_state_2")

        self.assertEqual(self.state.velocity, 50)
        self.assertEqual(self.state.altitude, 10000)
        self.assertEqual(self.state.range, 100000)

        y = 26436.3
        self.assertAlmostEqual(self.state.pressure, y, delta=y*testMargin)
        y = 223.15
        self.assertAlmostEqual(self.state.temperature, y, delta=y*testMargin)
        y = 0.412707
        self.assertAlmostEqual(self.state.density, y, delta=y*testMargin)
        y = 299.463
        self.assertAlmostEqual(self.state.speed_of_sound, y, delta=y*testMargin)
