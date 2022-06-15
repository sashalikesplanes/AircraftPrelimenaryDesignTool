from misc.constants import g, energyDensityHydrogen
import numpy as np



def calculate_crit_range(aircraft, range_to_crit):
    """
    Calculate the range that can be reached if at the critical point the biggest fuel tank (forward) is ruptured and all the fuel in it is lost
    """

    # Fuel used to get to critical point
    power = aircraft.FuselageGroup.Power
    fuel_fraction_cruise_to_crit, _ = power.get_fuel_fractions(range_to_crit, 0)
    fuel_fraction_to_crit = power.fuel_fraction_misc * fuel_fraction_cruise_to_crit

    fuel_used = aircraft.mtom - aircraft.mtom * fuel_fraction_to_crit
    fuel_remaining = aircraft.fuel_mass - fuel_used

    # Fuel and mass remaining at critical point after fuel tank burst
    forward_max_fuel = aircraft.FuselageGroup.Fuselage.ForwardFuelContainer.mass_H2
    fuel_in_forward = forward_max_fuel * fuel_remaining / aircraft.fuel_mass

    fuel_remaining -= fuel_in_forward
    
    zero_fuel_mass = aircraft.mtom - aircraft.fuel_mass
    fuel_fraction_remaining = zero_fuel_mass / (zero_fuel_mass + fuel_remaining)

    range_ = calc_range(zero_fuel_mass + fuel_remaining, zero_fuel_mass, aircraft)

    return range_

    # Range with the fuel remaining plus landing



def calc_range(W0, W1, aircraft):

    power = aircraft.FuselageGroup.Power
    prop_eff = power.propulsive_efficiency
    c_p = 1 / power.hydrogen_energy_density

    # TODO: implement realistic L/D
    L = (aircraft.mtom - 0.5 * (W0 - W1)) * 9.81
    D = aircraft.cruise_drag
    L_over_D_cruise = L / D

    # Range formula from ADSEE I
    power = aircraft.FuselageGroup.Power

    result = (prop_eff / g / c_p) * L_over_D_cruise * np.log(W0 / W1)

    return max(result, 0)

