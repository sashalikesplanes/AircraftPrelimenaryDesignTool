import numpy as np
from misc.constants import g
from sympy import Eq, Symbol, solve, sin, cos, tan
import matplotlib.pyplot as plt

def positive_real(lst):
    return [x for x in lst if x > 0 and np.imag(x) == 0] or None


def get_climb_rate(aircraft):
    rho = aircraft.states['cruise'].density
    wingloading = aircraft.WingGroup.Wing.wing_area
    CDmin = aircraft.C_D_min
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    efficiency = aircraft.WingGroup.Engines.propulsive_eff*aircraft.WingGroup.Engines.eff_mot_inv
    power = aircraft.WingGroup.Engines.P_motor*aircraft.WingGroup.Engines.own_amount_fans
    weight = aircraft.mtom * g
    k = 1 / (np.pi * A * e)

    V_best_ROC = np.sqrt(2 / rho * wingloading * np.sqrt(k / (3 * CDmin)))
    ROC_max = efficiency * power / weight - V_best_ROC * np.sqrt(4 * k * CDmin) * (1 / np.sqrt(3) + np.sqrt(3)) / 2
    return ROC_max, V_best_ROC

# V_best_climbangle^4+efficiency*power/(rho*S*CDmin)*V_best_climbangle-wingloading**2*4*k/(rho**2*CDmin)

def get_climb_angle_speed(aircraft):
    rho = aircraft.states['take-off'].density
    wingloading = aircraft.WingGroup.Wing.wing_area
    CDmin = aircraft.C_D_min
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    efficiency = aircraft.WingGroup.Engines.propulsive_eff * aircraft.WingGroup.Engines.eff_mot_inv
    power = aircraft.WingGroup.Engines.P_motor * aircraft.WingGroup.Engines.own_amount_fans
    S = aircraft.WingGroup.Wing.wing_area
    thrust_over_weight = aircraft.thrust_over_weight_takeoff
    V = aircraft.states['take-off'].velocity
    k = 1 / (np.pi * A * e)
    coeff = [1, 0, 0, efficiency*power/(rho*S*CDmin), -wingloading**2*4*k/(rho**2*CDmin)]
    #print(np.real(np.roots(coeff)))
    print('banana',thrust_over_weight,V,power,wingloading)
    V_best_climbangle = float(positive_real(np.roots(coeff))[0])
    #print(float(positive_real(np.roots(coeff))[0]))
    x1 = Symbol('x1', real=True)



    constant_1 = k * wingloading / (0.5 * rho * V ** 2)
    constant_2 = thrust_over_weight - 0.5*rho*V**2*CDmin/wingloading
    print('c1',constant_1,'c2',constant_2)
    a = solve([sin(x1) + constant_1 * cos(x1) ** 2 - constant_2], x1)
    for i in list(a):
        print('hello',i)
    print(float(a[0][0]))
    return V_best_climbangle






#sin(climb_angle) = thrust_over_weight - 0.5*rho*V**2/wing_loading*CDmin-k*wing_loading*cos(climb_angle)**2/(0.5*rho*V**2)
#Do this using a GR becaus python does not like it

# TODO make the plot
def get_power_plot(aircraft):
    V = np.arange(0,220,1)
    V_powered3 = np.power(V,3)
    rho = aircraft.states['cruise'].density
    CD = aircraft.C_D_min + aircraft.C_D_induced
    print(aircraft.C_D_min,aircraft.C_D_TO,CD)
    efficiency = aircraft.WingGroup.Engines.propulsive_eff*aircraft.WingGroup.Engines.eff_mot_inv
    power_available = aircraft.WingGroup.Engines.P_motor*aircraft.WingGroup.Engines.own_amount_fans * efficiency
    S = aircraft.WingGroup.Wing.wing_area
    power_available_array = np.ones(len(V))*power_available
    power_required_array = CD * 0.5*rho*V_powered3 * S

    plt.figure()
    plt.plot(V, power_required_array)
    plt.plot(V, power_available_array)


