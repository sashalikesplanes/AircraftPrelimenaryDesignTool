import numpy as np
from misc.constants import g
from sympy import Eq, Symbol, solve, sin, cos, tan
import matplotlib.pyplot as plt
from misc.ISA import getDensity, getSpeedOfSound

def positive_real(lst):
    return [x for x in lst if x > 0 and np.imag(x) == 0] or None


def get_max_climb_rate(aircraft):
    wingloading = aircraft.mtom * g / aircraft.WingGroup.Wing.wing_area
    CDmin = aircraft.C_D_min
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    efficiency = aircraft.WingGroup.Engines.propulsive_eff * aircraft.WingGroup.Engines.eff_mot_inv
    power = aircraft.WingGroup.Engines.P_motor * aircraft.WingGroup.Engines.own_amount_fans
    weight = aircraft.mtom * g
    k = 1 / (np.pi * A * e)

    rho = aircraft.states['cruise'].density
    V_best_ROC = np.sqrt(2 / rho * wingloading * np.sqrt(k / (3 * CDmin)))
    ROC_max = efficiency * power / weight - V_best_ROC * np.sqrt(4 * k * CDmin) * (1 / np.sqrt(3) + np.sqrt(3)) / 2
    return ROC_max, V_best_ROC


def calc_ROC(aircraft, state, V):
    if state == True:
        #Take-off
        rho = aircraft.states['take-off'].density
        #V = aircraft.takeoff_speed
    else:
        #cruise
        rho = aircraft.states['cruise'].density
        #V = aircraft.states['cruise'].velocity
    CDmin = aircraft.C_D_min
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    efficiency = aircraft.WingGroup.Engines.propulsive_eff * aircraft.WingGroup.Engines.eff_mot_inv
    power = aircraft.WingGroup.Engines.P_motor * aircraft.WingGroup.Engines.own_amount_fans
    weight = aircraft.mtom * g
    k = 1 / (np.pi * A * e)
    S = aircraft.WingGroup.Wing.wing_area
    CDi = (weight / (0.5 * rho * V ** 2 * S))**2*k
    Drag = (CDmin + CDi) * 0.5 * rho * V ** 2 * S
    ROC = (power*efficiency-V*Drag)/weight
    #print(power*efficiency, V*Drag)
    return ROC

# V_best_climbangle^4+efficiency*power/(rho*S*CDmin)*V_best_climbangle-wingloading**2*4*k/(rho**2*CDmin)

def get_climb_angle(aircraft,V):
    rho = aircraft.states['take-off'].density
    wingloading = aircraft.mtom*g/1.5/aircraft.WingGroup.Wing.wing_area
    CDmin = aircraft.C_D_min
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    thrust_over_weight = aircraft.thrust_over_weight_takeoff
    k = 1 / (np.pi * A * e)
    # efficiency = aircraft.WingGroup.Engines.propulsive_eff * aircraft.WingGroup.Engines.eff_mot_inv
    # power = aircraft.WingGroup.Engines.P_motor * aircraft.WingGroup.Engines.own_amount_fans
    # S = aircraft.WingGroup.Wing.wing_area
    #coeff = [1, 0, 0, efficiency*power/(rho*S*CDmin), -wingloading**2*4*k/(rho**2*CDmin)]
    #V_best_climbangle = float(positive_real(np.roots(coeff))[0])
    V_best_climbangle = V*1
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
    #print(aircraft.C_D_min,aircraft.C_D_TO,CD)
    efficiency = aircraft.WingGroup.Engines.propulsive_eff*aircraft.WingGroup.Engines.eff_mot_inv
    power_available = aircraft.WingGroup.Engines.P_motor*aircraft.WingGroup.Engines.own_amount_fans * efficiency

    power_available_array = np.ones(len(V))*power_available/10**6
    power_required_array = CD * 0.5*rho*V_powered3 * S/10**6

    plt.figure()
    plt.plot(V, power_required_array, label = "Power required")
    plt.plot(V, power_available_array, label = "Power available")
    plt.xlabel("Velocity [m/s]")
    plt.ylabel("Power [MW]")
    plt.legend()

def get_ROC_V_plot(aircraft):
    V = np.arange(20, 240, 1)
    lstcruise =[]
    lsttakeoff =[]
    for i in V:
        rocto = calc_ROC(aircraft, True, i)
        roccr = calc_ROC(aircraft, False, i)
        lstcruise.append(roccr)
        lsttakeoff.append(rocto)
    plt.figure()
    plt.plot(V, lsttakeoff, label = "Take-off density")
    plt.plot(V, lstcruise, label = "Cruise density")
    plt.xlabel("Velocity [m/s]")
    plt.ylabel("ROC [m/s]")
    plt.ylim(0)
    plt.legend()

def get_theta_plot(aircraft):
    V = np.arange(20, 220, 1)
    lstq = []
    for i in V:
        theta = get_climb_angle(aircraft,i)
        lstq.append(theta)
    plt.figure()
    plt.plot(V, lstq)

def get_heigt_velocity_plot(aircraft):
    Vlist = np.arange(1,200,10)
    rholist = np.arange(0.05, 1.225, 0.005)
    wingloading = aircraft.mtom * g / aircraft.WingGroup.Wing.wing_area
    CDmin = aircraft.C_D_min
    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    efficiency = aircraft.WingGroup.Engines.propulsive_eff * aircraft.WingGroup.Engines.eff_mot_inv
    power = aircraft.WingGroup.Engines.P_motor * aircraft.WingGroup.Engines.own_amount_fans
    weight = aircraft.mtom * g
    k = 1 / (np.pi * A * e)
    lst = []
    lst2 = []
    for rhoq in rholist:
        V_best_ROC = np.sqrt(2 / rhoq * wingloading * np.sqrt(k / (3 * CDmin)))
        ROC_max = efficiency * power / weight - np.sqrt(2 / rhoq * wingloading * np.sqrt(k / (3 * CDmin))) * np.sqrt(
            4 * k * CDmin) * (1 / np.sqrt(3) + np.sqrt(3)) / 2
        lst.append(ROC_max)
        lst2.append(V_best_ROC)
    plt.figure()
    plt.plot(lst, rholist)
    plt.ylabel("density")
    plt.xlabel("ROC")
    plt.show()
    plt.plot(lst2, rholist)


def get_performance_altitude_plot(aircraft):
    wingloading = aircraft.weight_over_surface
    CLmax = aircraft.C_L_max

    A = aircraft.WingGroup.Wing.aspect_ratio
    e = aircraft.WingGroup.Wing.oswald
    k = 1/(np.pi*A*e)
    CDmin = aircraft.C_D_min


    hlist=np.arange(0,11000,10)
    Vslist = []
    Vroclist = []
    Vplimlist = []
    for h in hlist:

        Vs = np.sqrt(2/getDensity(h)*wingloading/CLmax)
        Vslist.append(Vs)

        V_best_ROC = np.sqrt(2 / getDensity(h) * wingloading * np.sqrt(k / (3 * CDmin)))
        Vroclist.append(V_best_ROC)

        #coeff = [CDmin*0.5*getDensity(h)*S, 0, 0, -efficiency*power, k*weight**2/(0.5*getDensity(h)*S)]
        #Vplimit = float(positive_real(np.roots(coeff))[0])
        #Vplimlist.append(Vplimit)

        Mallowed = 0.65
        Vmach = Mallowed*getSpeedOfSound(h)
        Vplimlist.append(Vmach)

    plt.figure()
    plt.plot(Vslist,hlist, label ="Stall limit")
    plt.plot(Vroclist,hlist, label = 'Maximum rate of climb')
    plt.plot(Vplimlist,hlist, label = 'Mach limit')
    plt.plot([158,191.7],[11000,11000], label = "Altitude limit") # due to pressurization??????????
    plt.xlabel("Velocity [m/s]")
    plt.ylabel('Altitude [m]')
    plt.legend()
