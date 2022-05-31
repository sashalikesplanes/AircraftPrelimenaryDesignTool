import unittest
from pathlib import Path

from misc.constants import testMargin
from misc.openData import openData
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft


class TestSizing(unittest.TestCase):

    def setUp(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"test_state_1": State('test_state_1'), "cruise": State("test_state_2")}
        self.aircraft = Aircraft(openData(config_file), states)

        #Define test params
        self.aircraft.FuselageGroup.Aircraft.reference_area = 50  # [m2]

        self.aircraft.WingGroup.Wing.mean_geometric_chord = 6  # [m]
        self.aircraft.WingGroup.Wing.span = 20  # [m]

        self.aircraft.FuselageGroup.Fuselage.diameter = 10 # [m]

        self.aircraft.FuselageGroup.Tail.HorizontalTail.volume_coefficient = 0.9 # [-]
        self.aircraft.FuselageGroup.Tail.HorizontalTail.aspect_ratio = 5 # [-]
        self.aircraft.FuselageGroup.Tail.HorizontalTail.taper = 0.2 # [-]

        self.aircraft.FuselageGroup.Tail.VerticalTail.volume_coefficient = 0.05 # [-]
        self.aircraft.FuselageGroup.Tail.VerticalTail.aspect_ratio = 2 # [-]
        self.aircraft.FuselageGroup.Tail.VerticalTail.taper = 0.2 # [-]


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

    def test_horizontal_tail_sizing(self):
        self.aircraft.FuselageGroup.Tail.HorizontalTail.size_self_geometry()

        #Test tail length
        model_tail_length = self.aircraft.FuselageGroup.Tail.HorizontalTail.tail_length # [kg]
        analytical_tail_length =  4.145929794   # [m]
        self.assertAlmostEqual(model_tail_length, analytical_tail_length, delta = analytical_tail_length * testMargin)

        #Test surface area
        model_surface_area = self.aircraft.FuselageGroup.Tail.HorizontalTail.surface_area # [kg]
        analytical_surface_area = 65.12411291    # [m2]
        self.assertAlmostEqual(model_surface_area, analytical_surface_area, delta = analytical_surface_area * testMargin)

        #Test span
        model_span = self.aircraft.FuselageGroup.Tail.HorizontalTail.span # [kg]
        analytical_span = 18.04495953    # [m]
        self.assertAlmostEqual(model_span, analytical_span, delta = analytical_span * testMargin)

        #Test mean geometric chord
        model_mean_aerodynamic_chord = self.aircraft.FuselageGroup.Tail.HorizontalTail.mean_geometric_chord # [kg]
        analytical_mean_aerodynamic_chord = 4.143657374   # [kg]
        self.assertAlmostEqual(model_mean_aerodynamic_chord, analytical_mean_aerodynamic_chord, delta = analytical_mean_aerodynamic_chord * testMargin)


    def test_vertical_tail_sizing(self):
        self.aircraft.FuselageGroup.Tail.VerticalTail.size_self_geometry()

        #Test tail length
        model_tail_length = self.aircraft.FuselageGroup.Tail.VerticalTail.tail_length # [kg]
        analytical_tail_length =  1.784124116   # [m]
        self.assertAlmostEqual(model_tail_length, analytical_tail_length, delta = analytical_tail_length * testMargin)

        #Test surface area
        model_surface_area = self.aircraft.FuselageGroup.Tail.VerticalTail.surface_area # [kg]
        analytical_surface_area = 28.02495608    # [m2]
        self.assertAlmostEqual(model_surface_area, analytical_surface_area, delta = analytical_surface_area * testMargin)

        #Test span
        model_span = self.aircraft.FuselageGroup.Tail.VerticalTail.span # [kg]
        analytical_span = 7.486648928    # [m]
        self.assertAlmostEqual(model_span, analytical_span, delta = analytical_span * testMargin)

        #Test mean geometric chord
        model_mean_aerodynamic_chord = self.aircraft.FuselageGroup.Tail.VerticalTail.mean_geometric_chord # [kg]
        analytical_mean_aerodynamic_chord = 4.297891051  # [kg]
        self.assertAlmostEqual(model_mean_aerodynamic_chord, analytical_mean_aerodynamic_chord, delta = analytical_mean_aerodynamic_chord * testMargin)



