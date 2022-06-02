import numpy as np
import matplotlib.pyplot as plt
import misc.constants as const
from pathlib import Path
from misc.ISA import getDensity


def make_flight_envelope(aircraft, test_state):
    altitude = aircraft.states[test_state].altitude
    rho = getDensity(altitude)
    wing_span = aircraft.WingGroup.Wing.span
    wing_area = aircraft.WingGroup.Wing.wing_area
    MGC = aircraft.WingGroup.Wing.mean_geometric_chord
    W = aircraft.mtom * const.g
    W_ZF = W - aircraft.fuel_mass * const.g
    W_min = W - aircraft.payload_mass * const.g - aircraft.fuel_mass * const.g
    W_max_landing = W - aircraft.fuel_mass * const.g * 0.8 #TODO: make sure it's reasonable
    wing_loading = aircraft.weight_over_surface
    C_L_alpha = np.rad2deg(aircraft.WingGroup.Wing.C_L_alpha) # [1/rad]
    C_L_max = aircraft.C_L_max
    C_L_min = aircraft.WingGroup.Wing.C_L_min
    delta_C_L_TO = 1
    delta_C_L_land = 1.3 
    V_H = 200 # TODO: Get number somewhere
    V_C_max = aircraft.states[test_state].velocity
    V_D = V_C_max * 1.25
    n_neg = -1
    n_pos_HLD = 2
    n_neg_HLD = 0
    max_alt = 7000



    n_pos = get_n_pos(W)
    V_stall = np.sqrt(W / (0.5 * rho * C_L_max * wing_area))
    V_stall_inverted = np.sqrt(W / (0.5 * rho * abs(C_L_min) * wing_area))
    V_G = np.sqrt(2 * abs(n_neg) * W / (rho * wing_area * abs(C_L_min)))
    V_A = np.sqrt(n_pos) * V_stall


    # TODO rho from ISA
    Vs = np.linspace(0, V_D )
    n_V_G = 0.5 * rho * V_G**2 * wing_area * C_L_min / W
    Vs_prime = np.linspace(V_stall, V_A )
    positive_stall_line = 0.5 * rho * Vs_prime**2 * wing_area * C_L_max / W

    plt.plot(Vs_prime, positive_stall_line, 'k')
    plt.hlines(n_neg, V_G, V_D, colors='k')
    plt.hlines(0, 0, 1.25*V_D, colors='grey')
    plt.hlines(n_pos, V_A, V_D, colors='k')
    plt.vlines(V_D, n_neg, n_pos, colors='k')
    plt.vlines(V_stall, 0, 1, colors='k')
    plt.vlines(V_stall_inverted, n_neg, 0, colors='k')

    R_1 = W_max_landing / W
    R_2 = W_ZF / W
    F_gm = np.sqrt(R_2 * np.tan(np.pi * R_1 / 4))
    F_gz = 1 - max_alt / 76200
    F_g = 0.5 * (F_gz + F_gm)
    H = 107
    Hs = np.arange(9,109, 11)
    U_ref = 17.07 - (17.07-13.41)/4572 * altitude
    U_ds = U_ref * F_g * (H/107)**(1/6)
    U_ds_prime = 0.5 * U_ds
    mu_g = 2 * wing_loading  / (rho * MGC * C_L_alpha * 9.81)
    K_g = 0.88 * mu_g / (5.3 + mu_g)
    gust_lines = get_gust_load(K_g, U_ds, Vs, C_L_alpha, wing_loading)
    gust_lines_prime = get_gust_load(K_g, U_ds_prime, Vs, C_L_alpha, wing_loading)
    
    gust_lines_neg = get_gust_load(K_g, -U_ds, Vs, C_L_alpha, wing_loading)
    gust_lines_prime_neg = get_gust_load(K_g, -U_ds_prime, Vs, C_L_alpha, wing_loading)

    plt.plot(Vs, gust_lines, 'k')
    plt.plot(Vs, gust_lines_prime, 'k')
    plt.plot(Vs, gust_lines_neg, 'k')
    plt.plot(Vs, gust_lines_prime_neg, 'k')

    # Check At V_A gust > Manoeuvre
    # V_A manoeuvre
    # plt.plot(V_A, n_pos, marker="o", markersize=10)
    n_gust_a = get_gust_load(K_g, U_ds, V_A, C_L_alpha, wing_loading)
    # plt.plot(V_A, n_gust_a, marker="o", markersize=10)
    n_diff = (n_pos - n_gust_a)


    # V_A gust
    if n_diff < 0:
        V_A_new = np.roots([0.5 * rho * C_L_max, -K_g * U_ds * C_L_alpha \
                * 0.610, -wing_loading])
        n_gust_a_new = get_gust_load(K_g, U_ds, max(V_A_new), C_L_alpha, wing_loading)
        # plt.plot(max(V_A_new), n_gust_a_new, marker="o", markersize=10)
        print(max(V_A_new))


    # V_C gust
    n_cruise = get_gust_load(K_g, U_ds, V_C_max, C_L_alpha, wing_loading)
    if n_cruise > n_pos:
        plt.plot(V_C_max, n_cruise, 'k', marker="o", markersize=10)



        # V_D minigust
        n_dive = get_gust_load(K_g, U_ds_prime, V_D, C_L_alpha, wing_loading)
        # plt.plot(V_D, n_dive, marker="o", markersize=10)
        plt.plot([V_C_max, V_D], [n_cruise, n_dive], 'k')

    # Negative same 
    V_intersect = 498 * 1/47.88 * wing_loading * (1 - n_neg)/(K_g * U_ds * 3.281 * C_L_alpha * 1.9438)
    n_cruise_neg = get_gust_load(K_g, - U_ds, V_C_max, C_L_alpha, wing_loading)
    if n_cruise_neg < n_neg:
    # plt.plot(V_C_max, n_cruise_neg, marker="o", markersize=10)
        n_dive_neg = get_gust_load(K_g, - U_ds_prime, V_D, C_L_alpha, wing_loading)
        plt.plot([V_C_max, V_D], [n_cruise_neg, n_dive_neg], 'k')
    if V_intersect < V_C_max:
        plt.plot([V_intersect, V_C_max], [n_neg, n_cruise_neg], 'k')

    if V_intersect < V_D:
        plt.plot(V_intersect, n_neg, 'k', marker="o", markersize=10)
        

    if altitude < 300:
        # Take off
        V_stall_TO = np.sqrt(2 * W/ (rho * (C_L_max + delta_C_L_TO) * wing_area))
        V_F_TO = 1.6 * V_stall_TO
        V_A_TO = V_stall_TO * np.sqrt(n_pos_HLD)

        V_TO = np.linspace(V_stall_TO, V_A_TO)
        positive_stall_line_TO = 0.5 * rho * V_TO**2 * wing_area * (C_L_max + delta_C_L_TO) / W
        plt.vlines(V_F_TO, 0, 2, colors='k')
        plt.hlines(2, V_A_TO, V_F_TO, colors='k')
        plt.vlines(V_stall_TO, 0, 1, colors='k')
        plt.plot(V_TO, positive_stall_line_TO, 'k')


        # Land
        V_stall_land = np.sqrt(2 * W_max_landing / (rho * (C_L_max + delta_C_L_land) * wing_area))
        V_F_land = 1.8 * V_stall_land
        V_A_land = V_stall_land * np.sqrt(n_pos_HLD)
        V_land = np.linspace(V_stall_land, V_A_land)
        positive_stall_line_land = 0.5 * rho * V_land**2 * wing_area * (C_L_max + delta_C_L_land) / W_max_landing
        plt.vlines(V_F_land, 0, 2, colors='k')
        plt.hlines(2, V_A_land, V_F_land, colors='k')
        plt.vlines(V_stall_land, 0, 1, colors='k')
        plt.plot(V_land, positive_stall_line_land, 'k')







    plt.title("GET LIMIT LOADS AND MULTIPLY BY 1.5 TO GET ULTIMATE LOADS")
    figpath = Path("plots", f'flightEnvelope{test_state}')
    plt.savefig(figpath, dpi=600)
    plt.cla()


def get_gust_load(K_g, U_ds, V, C_L_alpha, wing_loading):
    n_g = 1 + (K_g * U_ds * V * 1.944 * 3.281 * C_L_alpha) / (498 * 0.021 * wing_loading)
    return n_g 


def get_n_pos(W):
    load_factor = 2.1 + 24000 / (W + 10000)
    if load_factor <= 2.5:
        return 2.5
    elif load_factor <= 3.8:
        return load_factor
    else:
        return 3.8


