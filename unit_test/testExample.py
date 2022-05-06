import unittest
from misc.constants import testMargin


class TestExample(unittest.TestCase):
    def test_addition(self):
        x = {}

        self.assertAlmostEqual(y, f(x), delta=y*testMargin)


# class TestObjects(unittest.TestCase):
#     def test_passenger(self):
#         name = "John Doe"
#         mass = 75
#         arm = 100
#         person = Passenger(name, mass, arm)
#         self.assertEqual(person.mass, mass)
#         self.assertEqual(person.name, name)
#         self.assertEqual(person.arm, arm * 0.0254)
#
#     def test_plane(self):
#         plane = Plane(7500, 2500)
#         self.assertAlmostEqual(10000 / 2.20462, plane.mass, delta=(10000 / 2.20462) * 0.02)
#
#     def test_cog(self):
#         aircraft = Plane(9165, 2800)
#
#         aircraft.board(Passenger("Pilot 1", 92, 3.3274 * 39.3701))
#         aircraft.board(Passenger("Pilot 2", 103, 3.3274 * 39.3701))
#         aircraft.board(Passenger("Coordinator 1", 90, 4.318 * 39.3701))
#         aircraft.board(Passenger("Coordinator 2", 69, 4.318 * 39.3701))
#
#         aircraft.board(Passenger("1L", 61, 5.4356 * 39.3701))
#         aircraft.board(Passenger("1R", 78, 5.4356 * 39.3701))
#         aircraft.board(Passenger("2L", 64, 6.3754 * 39.3701))
#         aircraft.board(Passenger("2R", 69, 6.3754 * 39.3701))
#         aircraft.board(Passenger("3L", 83, 7.3152 * 39.3701))
#         aircraft.board(Passenger("3R", 84, 7.3152 * 39.3701))
#
#         # Passengers are neglected as their weight will most likely not significantly affect the cog position
#         self.assertAlmostEqual(aircraft.calculateCOG(dFuel=283 * 0.453592), 7.0931, delta=7.0931 * 0.02)
#
#     def test_cgshift_passenger(self):
#         aircraft = Plane(9165, 300)
#         aircraft.board(Passenger("human", 453.592, 50))
#
#         x0 = aircraft.calculateCOG(dFuel=0)
#         aircraft.move_passenger("human", 2.54)
#         x1 = aircraft.calculateCOG(dFuel=0)
#
#         self.assertAlmostEqual(-0.121356904, x0 - x1, delta=abs(-0.121356904 * 0.002))
#
#     def test_cgshift_fuel(self):
#         aircraft = Plane(9165, 300)
#
#         x0 = aircraft.calculateCOG(dFuel=0)
#         x1 = aircraft.calculateCOG(dFuel=45.3592)  # dFuel = 100 pounds
#
#         self.assertAlmostEqual(-0.00102892, x0 - x1, delta=abs(-0.00102892 * 0.002))
#         pass
