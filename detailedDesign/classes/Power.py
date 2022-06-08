import numpy as np

from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuelCells import FuelCells


class Power(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)

        self.FuselageGroup = FuselageGroup

        self.FuelCells = FuelCells(self, self.design_config)
        # self.Batteries = Batteries(self, self.design_config)
        self.components = [self.FuelCells]

        self.own_power_average = None
        self.own_power_peak = None
        self.reserve_mass_H2 = None
        self.mass_H2 = None

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        cruise_state = self.FuselageGroup.Aircraft.states['cruise']
        P_motor = self.FuselageGroup.Aircraft.WingGroup.Engines.P_motor
        n_motor = self.FuselageGroup.Aircraft.WingGroup.Engines.amount_motor
        percent_prop = self.percentage_propulsion_power
        eff_converter = self.eff_converter
        cable_contingency = self.cable_contingency
        T_avg = self.FuselageGroup.Aircraft.cruise_drag
        V = cruise_state.velocity 

        # necessary power output from fuel cells + taking into account cable losses
        P_avg_prop = T_avg * V 
        P_rest_aircraft = (P_avg_prop / percent_prop) * (1-percent_prop)
        #P_required_avg = P_avg_prop / (percent_prop * eff_converter) * cable_contingency

        P_required_peak = ((n_motor * P_motor) + P_rest_aircraft) / eff_converter * cable_contingency

        #self.own_power_average = P_required_avg
        self.own_power_peak = P_required_peak

        self.pos = np.array([0, 0., 0.])

        # Fuel mass sizing
        peakpower = self.own_power_peak
        averagepower = self.own_power_average
        duration_peak = 0.5  # [h] TODO: find the right value (Take off, etc...)
        mass_H2_peak = peakpower * duration_peak / (
                32167 * self.FuselageGroup.Power.FuelCells.conversion_efficiency)
        mass_H2_average = averagepower * (cruise_state.duration / 3600 - duration_peak) / (
                32167 * self.FuselageGroup.Power.FuelCells.conversion_efficiency)
        self.reserve_mass_H2 = averagepower * self.FuselageGroup.Aircraft.reserve_duration \
                               / (32167 * self.FuselageGroup.Power.FuelCells.conversion_efficiency)

        self.mass_H2 = mass_H2_peak + mass_H2_average + self.reserve_mass_H2
