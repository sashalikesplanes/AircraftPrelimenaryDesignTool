# To check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuelCells import FuelCells
from detailedDesign.classes.Batteries import Batteries
import numpy as np

class Power(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)

        self.FuselageGroup = FuselageGroup

        self.FuelCells = FuelCells(self, self.design_config)
        self.Batteries = Batteries(self, self.design_config)
        self.components = [self.FuelCells, self.Batteries]

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        P_motor = Engines.P_motor
        n_motor = self.FuselageGroup.Aircraft.WingGroup.Engines.amount_motor
        percent_prop = self.percentage_propulsion_power
        eff_inverter = self.eff_inverter
        eff_converter = self.eff_converter
        cable_contingency = self.cable_contingency

        #necessary power output from fuel cells
        P_output_fuelcells = (n_motor * P_motor) / (percent_prop * eff_inverter * eff_converter)

        #taking into account cable losses, thus required power from fuel cells
        P_required = P_output_fuelcells * cable_contingency

        self.own_power = P_required

