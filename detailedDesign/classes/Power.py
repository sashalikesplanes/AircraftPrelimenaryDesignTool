# To check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuelCells import FuelCells
import numpy as np


class Power(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)

        self.FuselageGroup = FuselageGroup

        self.FuelCells = FuelCells(self, self.design_config)
        # self.Batteries = Batteries(self, self.design_config)
        self.components = [self.FuelCells]
        self.own_power = None

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        P_motor = self.FuselageGroup.Aircraft.WingGroup.Engines.P_motor
        n_motor = self.FuselageGroup.Aircraft.WingGroup.Engines.amount_motor
        percent_prop = self.percentage_propulsion_power
        eff_inverter = self.eff_inverter
        eff_converter = self.eff_converter
        cable_contingency = self.cable_contingency
        T_avg = self.FuselageGroup.Aircraft.cruise_drag
        V = self.FuselageGroup.Aircraft.states['cruise'].velocity

        # necessary power output from fuel cells + taking into account cable losses
        P_avg_prop = T_avg * V
        P_rest_aircraft = (P_avg_prop / percent_prop) * (1-percent_prop)
        P_required_avg = P_avg_prop / \
            (percent_prop * eff_inverter * eff_converter) * cable_contingency

        P_required_peak = ((n_motor * P_motor) + P_rest_aircraft) / \
            (eff_inverter * eff_converter) * cable_contingency

        self.own_power_average = P_required_avg
        self.own_power_peak = P_required_peak
