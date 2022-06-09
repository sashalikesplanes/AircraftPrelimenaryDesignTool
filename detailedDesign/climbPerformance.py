import numpy as np
from misc.constants import g
from sympy import Eq, Symbol, solve, sin, cos, tan
import matplotlib.pyplot as plt

def positive_real(lst):
    return [x for x in lst if x > 0 and np.imag(x) == 0] or None


def get_climb_rate(aircraft, optimal_velocity):
    rholist = np.arange(0.05, 1.225, 0.005)
    rho = aircraft.states['cruise'].density
    wingloading = aircraft.mtom * g / aircraft.WingGroup.Wing.wing_area
    CDmin = aircraft.C_D_min
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    efficiency = aircraft.WingGroup.Engines.propulsive_eff * aircraft.WingGroup.Engines.eff_mot_inv
    power = aircraft.WingGroup.Engines.P_motor * aircraft.WingGroup.Engines.own_amount_fans
    weight = aircraft.mtom * g
    k = 1 / (np.pi * A * e)
    lst = []
    for rhoq in rholist:
        if optimal_velocity:
            V_best_ROC = np.sqrt(2 / rhoq * wingloading * np.sqrt(k / (3 * CDmin)))
        else:
            V_best_ROC = aircraft.states['cruise'].velocity
        ROC_max = efficiency * power / weight - V_best_ROC * np.sqrt(4 * k * CDmin) * (1 / np.sqrt(3) + np.sqrt(3)) / 2
        lst.append(ROC_max)
    ## uncomment if a plot for climb ceiling is wanted. ceiling~~18km which is to high
    # plt.plot(lst, rholist)
    # plt.ylabel("density")
    # plt.xlabel("ROC")
    # plt.show()
    if optimal_velocity:
        V_best_ROC = np.sqrt(2 / rho * wingloading * np.sqrt(k / (3 * CDmin)))
    else:
        V_best_ROC = aircraft.states['cruise'].velocity
    ROC_max = efficiency * power / weight - V_best_ROC * np.sqrt(4 * k * CDmin) * (1 / np.sqrt(3) + np.sqrt(3)) / 2
    return ROC_max, V_best_ROC

# V_best_climbangle^4+efficiency*power/(rho*S*CDmin)*V_best_climbangle-wingloading**2*4*k/(rho**2*CDmin)

def get_climb_angle(aircraft):
    rho = aircraft.states['cruise'].density
    wingloading = aircraft.mtom*g/aircraft.WingGroup.Wing.wing_area
    CDmin = aircraft.C_D_min
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    efficiency = aircraft.WingGroup.Engines.propulsive_eff * aircraft.WingGroup.Engines.eff_mot_inv
    power = aircraft.WingGroup.Engines.P_motor * aircraft.WingGroup.Engines.own_amount_fans
    S = aircraft.WingGroup.Wing.wing_area
    thrust_over_weight = aircraft.thrust_over_weight_takeoff
    V = aircraft.states['cruise'].velocity
    k = 1 / (np.pi * A * e)
    V_best_climbangle = V * 1
    #coeff = [1, 0, 0, efficiency*power/(rho*S*CDmin), -wingloading**2*4*k/(rho**2*CDmin)]
    #V_best_climbangle = float(positive_real(np.roots(coeff))[0])
    #print(float(positive_real(np.roots(coeff))[0]))

    x1 = Symbol('x1', real=True)
    constant_1 = k * wingloading / (0.5 * rho * V_best_climbangle ** 2)
    constant_2 = thrust_over_weight - 0.5*rho*V_best_climbangle**2*CDmin/wingloading
    a = solve([sin(x1) + constant_1 * cos(x1) ** 2 - constant_2], x1)
    lst = []
    for i in list(a):
        lst.append(i[0])
    climb_angle = min(lst)
    return climb_angle*180/np.pi  # make it degrees






#sin(climb_angle) = thrust_over_weight - 0.5*rho*V**2/wing_loading*CDmin-k*wing_loading*cos(climb_angle)**2/(0.5*rho*V**2)
#Do this using a GR becaus python does not like it

# TODO make the plot
def get_power_plot(aircraft):
    V = np.arange(20,260,1)
    V_powered3 = np.power(V,3)
    rho = aircraft.states['cruise'].density
    S = aircraft.WingGroup.Wing.wing_area
    W = aircraft.mtom*g
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    CL = W/(0.5*rho*V**2*S)
    CDi = CL**2/(np.pi*A*e)
    CD = aircraft.C_D_min + CDi
    print(aircraft.C_D_min,aircraft.C_D_TO,CD)
    efficiency = aircraft.WingGroup.Engines.propulsive_eff*aircraft.WingGroup.Engines.eff_mot_inv
    power_available = aircraft.WingGroup.Engines.P_motor*aircraft.WingGroup.Engines.own_amount_fans * efficiency

    power_available_array = np.ones(len(V))*power_available
    power_required_array = CD * 0.5*rho*V_powered3 * S

    plt.figure()
    plt.plot(V, power_required_array)
    plt.plot(V, power_available_array)


