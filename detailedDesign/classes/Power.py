import numpy as np

from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuelCells import FuelCells
from misc.constants import g


class Power(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)

        self.FuselageGroup = FuselageGroup
        self.parent = self.FuselageGroup

        self.FuelCells = FuelCells(self, self.design_config)
        # self.Batteries = Batteries(self, self.design_config)
        self.components = [self.FuelCells]

        self.own_power_average = None
        self.own_power_peak = None
        self.reserve_mass_H2 = None
        self.mass_H2 = 1
        self.propulsive_efficiency = None

        self.fuel_fraction_misc = 1.0
        self.fuel_fraction_loiter = 1.0

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def get_fuel_fractions(self, range_, loiter_duration):

        cruise_state = self.FuselageGroup.Aircraft.states['cruise']

        average_cruise_lift = (self.FuselageGroup.Aircraft.mtom - self.mass_H2 / 2) * g 
        lift_over_drag = average_cruise_lift / self.FuselageGroup.Aircraft.cruise_drag

        specific_fuel_consumption = 1 / self.hydrogen_energy_density

        engines = self.FuselageGroup.Aircraft.WingGroup.Engines
        self.propulsive_efficiency = self.FuelCells.conversion_efficiency * self.eff_converter / self.cable_contingency * engines.eff_mot_inv * (engines.propulsive_eff + engines.increase_BLI_eff)

        fuel_fraction_cruise = np.exp(- range_ / lift_over_drag * g * specific_fuel_consumption / self.propulsive_efficiency)

        fuel_fraction_loiter = np.exp(- cruise_state.velocity * loiter_duration / lift_over_drag * g * specific_fuel_consumption / self.propulsive_efficiency)

        return fuel_fraction_cruise, fuel_fraction_loiter


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
        P_required_avg = P_avg_prop / (percent_prop * eff_converter) * cable_contingency

        P_required_peak = ((n_motor * P_motor) + P_rest_aircraft) / eff_converter * cable_contingency

        self.own_power_average = P_required_avg
        self.own_power_peak = P_required_peak

        self.pos = np.array([0, 0., 0.])

        #########################################################
        # Using fuel mass fractions method of finding fuel mass #
        #########################################################
        # Add takeoff, landing and climb fractions for jet fuel
        fuel_fraction_misc_jet = self.fuel_fraction_takeoff * self.fuel_fraction_climb * self.fuel_fraction_landing 
        self.fuel_fraction_misc = 1 - ((1 - fuel_fraction_misc_jet) * self.jet_fuel_energy_density / self.hydrogen_energy_density)

        loiter_duration = self.FuselageGroup.Aircraft.loiter_duration

        fuel_fraction_cruise, fuel_fraction_loiter = self.get_fuel_fractions(cruise_state.range, loiter_duration)

        fuel_fraction_total = self.fuel_fraction_misc * fuel_fraction_cruise * fuel_fraction_loiter

        self.logger.debug(f"{fuel_fraction_cruise = }")
        self.logger.debug(f"{self.fuel_fraction_loiter = }")
        self.logger.debug(f"{fuel_fraction_total = }")
        self.logger.debug(f"{self.propulsive_efficiency = }")

        self.mass_H2 = self.FuselageGroup.Aircraft.zero_fuel_mass / fuel_fraction_total - self.FuselageGroup.Aircraft.zero_fuel_mass
        self.logger.debug(f"{self.mass_H2 = }")
        


        # Fuel mass sizing
        # peakpower = self.own_power_peak
        # averagepower = self.own_power_average
        # duration_peak = 0.5  # [h] TODO: find the right value (Take off, etc...)
        # mass_H2_peak = peakpower * duration_peak / (
        #         32167 * self.FuselageGroup.Power.FuelCells.conversion_efficiency)
        # mass_H2_average = averagepower * (cruise_state.duration / 3600 - duration_peak) / (
        #         32167 * self.FuselageGroup.Power.FuelCells.conversion_efficiency)
        # self.reserve_mass_H2 = averagepower * self.FuselageGroup.Aircraft.reserve_duration \
        #                        / (32167 * self.FuselageGroup.Power.FuelCells.conversion_efficiency)
        # 
        # self.mass_H2 = mass_H2_peak + mass_H2_average + self.reserve_mass_H2
