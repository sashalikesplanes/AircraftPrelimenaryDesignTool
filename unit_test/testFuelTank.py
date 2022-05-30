import unittest
from pathlib import Path
from misc.constants import testMargin
from misc.openData import openData
from misc.unitConversions import *
from misc.ISA import *
from detailedDesign.classes.State import State
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.FuelCells import FuelCells


class TestFuelTank(unittest.TestCase):
    def setUp(self):
        config_file = Path('data', 'new_designs', 'config.yaml')
        states = {"test_state_1": State('test_state_1'), "cruise": State("test_state_2")}
        self.aircraft = Aircraft(openData(config_file), states)
        # self.aircraft.FuselageGroup.get_sized()

        # ----- Define test params -----
        self.aircraft.FuselageGroup.Power.own_power_peak = 100e6
        self.aircraft.FuselageGroup.Power.FuelCells.mass_power_density = 10000
        self.aircraft.FuselageGroup.Power.FuelCells.W_size = 1000

        # Fuel tank
        self.aircraft.FuselageGroup.Fuselage.inner_diameter = 10
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.thickness = 0.001


        # Imperial constants from test params:
        # l_FS = 492.12598    # [ft]
        # S_fus = 55308.51562 # [ft2]
        # W_o = 220462.2622   # [lbs]
        # l_HT = 270.74245    # [ft]
        # d_FS = 32.8084      # [ft]
        # q = 0.0080615       # [psi] for test_state_1
        # V_p = 277360.9475   # [ft3] for test_state_1
        # Delta_P = 0         # [psi] for test_state_1

    def test_fuel_cell(self):

        self.aircraft.FuselageGroup.Power.FuelCells.size_self()
        model_mass = self.aircraft.FuselageGroup.Power.FuelCells.mass
        model_size = self.aircraft.FuselageGroup.Power.FuelCells.size

        analytical_mass_kg = 10000
        analytical_size = 10
        print("mass: ", analytical_mass_kg)
        print("size: ", analytical_size)
        self.assertAlmostEqual(model_mass, analytical_mass_kg, delta=analytical_mass_kg * testMargin)
        self.assertAlmostEqual(model_size, analytical_size, delta=analytical_size * testMargin)


    def test_batteries(self):
        pass

    def test_removable_fuel_container(self):
        pass

    def test_non_removable_fuel_container(self):
        pass

    def test_fuel_container(self):
        self.aircraft.FuselageGroup.Fuselage.FuelContainer.size_self()

        model_thickness = self.aircraft.FuselageGroup.Fuselage.FuelContainer.thickness
        model_mass_H2 = self.aircraft.FuselageGroup.Fuselage.FuelContainer.mass_H2
        model_tank_volume = self.aircraft.FuselageGroup.Fuselage.FuelContainer.volume_tank
        model_tank_area = self.aircraft.FuselageGroup.Fuselage.FuelContainer.area_tank
        model_structural_mass = self.aircraft.FuselageGroup.Fuselage.FuelContainer.own_mass

        analytical_thickness = None
        analytical_mass_H2 = None
        analytical_tank_volume = None
        analytical_tank_area = None
        analytical_structural_mass = None