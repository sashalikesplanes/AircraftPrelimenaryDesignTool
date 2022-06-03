import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import logging

logger = logging.getLogger("logger")


def get_constraints(aircraft):
    """
    Produce a constraint diagram - W/S vs T/W
    """

    # Parameters needed
    aspect_ratio = aircraft.WingGroup.Wing.aspect_ratio
    oswald_efficiency = aircraft.WingGroup.Wing.get_oswald()
    lift_induced_drag_constant = 1 / (np.pi * aspect_ratio * oswald_efficiency)

    velocity = aircraft.states['cruise'].velocity
    density = aircraft.states['cruise'].density
    dynamic_pressure = 0.5 * density * velocity ** 2

    max_bank_angle = 40 / 180 * np.pi  # rad   #taken from regulation
    load_factor = 1 / np.cos(max_bank_angle)

    rho_takeoff_air = 1.225
    velocity_crit_takeoff = 27

    C_D_min = aircraft.C_D_min
    C_L_max = aircraft.C_L_max
    # from regulation I believe but I cannot find anything about it
    required_climb_rate = aircraft.required_climb_rate
    # therefore we take ot from the yamel and it is something we change in order to make it work
    C_L_TO = aircraft.C_L_TO
    C_D_TO = aircraft.C_D_TO
    # Start calculating the functions
    wing_loading_points = np.linspace(1000, 10000, 1000)

    # q using turning speed and associated altitude
    def thrust_loading_constant_turn_f(wing_loading):
        return dynamic_pressure * \
            (C_D_min / wing_loading + lift_induced_drag_constant *
             (load_factor / dynamic_pressure) ** 2 * wing_loading)
    
    def thrust_loading_climb_rate_f(wing_loading):
        return required_climb_rate / velocity + dynamic_pressure / \
            wing_loading * C_D_min + lift_induced_drag_constant / \
            dynamic_pressure * wing_loading

    def thrust_loading_cruise_f(wing_loading):
        return dynamic_pressure * C_D_min / wing_loading + \
            lift_induced_drag_constant / dynamic_pressure * wing_loading


    def thrust_loading_takeoff_f(wing_loading):
        return 1 / aircraft.FuselageGroup.Fuselage.hull_shape_factor - 1 / 13 * rho_takeoff_air * velocity_crit_takeoff ** 2 * C_L_TO / wing_loading + 0.5 * rho_takeoff_air * velocity_crit_takeoff ** 2 * C_D_TO / wing_loading

    thrust_loading_constant_turn = thrust_loading_constant_turn_f(wing_loading_points) 
    thrust_loading_climb_rate = thrust_loading_climb_rate_f(wing_loading_points)
    thrust_loading_cruise = thrust_loading_cruise_f(wing_loading_points)
    thrust_loading_takeoff = thrust_loading_takeoff_f(wing_loading_points)
    # q using climb airspeed and associated altitude


    q_stall = 0.5 * density * aircraft.clean_stall_speed ** 2
    weight_over_surface_stall = C_L_max * q_stall
 #   logger.debug(f"{ C_L_max = }")

    WS = weight_over_surface_stall
    logger.debug(f"{thrust_loading_constant_turn_f(WS) = }")
    TW = max(thrust_loading_constant_turn_f(WS), thrust_loading_climb_rate_f(WS), thrust_loading_cruise_f(WS), thrust_loading_takeoff_f(WS))

    # Plot the fuctions
    # fig, ax = plt.subplots()
    # 
    # ax.plot(wing_loading_points, thrust_loading_cruise,
    #         'r', label='Cruise speed')
    # ax.plot(wing_loading_points, thrust_loading_constant_turn,
    #         'b', label='Constant turn')
    # 
    # ax.plot(wing_loading_points, thrust_loading_climb_rate,
    #         'g', label='Climb rate')
    # 
    # ax.plot(wing_loading_points, thrust_loading_takeoff,
    #         'pink', label='Takeoff')
    # ax.vlines(weight_over_surface_stall, 0, 1)
    # 
    # ax.set_xlabel('W/S')
    # ax.set_ylabel('T/W')
    # 
    # plt.legend()
    # 
    # plt.show()

    # Calculate optimum
    # If they do not intersect
    # Calculate min of each
    # Optimum is the max of those
    # If they intersect
    # Calculate where they intersect
    # Calculate min of each
    # Optimum is the max of those

    # calculate intersections
    # thrust_intersections = []
    # weight_intersections = []
    # idx1 = np.argwhere(
    #     np.diff(np.sign(thrust_loading_cruise - thrust_loading_climb_rate))).flatten()
    # idx2 = np.argwhere(np.diff(
    #     np.sign(thrust_loading_cruise - thrust_loading_constant_turn))).flatten()
    # idx3 = np.argwhere(np.diff(
    #     np.sign(thrust_loading_climb_rate - thrust_loading_constant_turn))).flatten()

    # thrust_intersections += [thrust_loading_cruise[idx1],
    #                          thrust_loading_cruise[idx2], thrust_loading_climb_rate[idx3]]
    # thrust_intersections = list(filter(None, thrust_intersections))
    # weight_intersections += [wing_loading_points[idx1],
    #                          wing_loading_points[idx2], wing_loading_points[idx3]]
    # weight_intersections = list(filter(None, weight_intersections))
    # thrust_intersections = [i[0] for i in thrust_intersections]
    # weight_intersections = [i[0] for i in weight_intersections]

    # # calculate minimum of each curve
    # thrust_conditions = []
    # weight_conditions = []
    # thrust_loading_cruise = thrust_loading_cruise.tolist()
    # thrust_loading_climb_rate = thrust_loading_climb_rate.tolist()
    # thrust_loading_constant_turn = thrust_loading_constant_turn.tolist()
    # thrust_conditions += [min(thrust_loading_cruise),
    #                       min(thrust_loading_climb_rate), min(thrust_loading_constant_turn)]
    # weight_conditions += [wing_loading_points[thrust_loading_cruise.index(min(thrust_loading_cruise))], wing_loading_points[thrust_loading_climb_rate.index(min(thrust_loading_climb_rate))],
    #                       wing_loading_points[thrust_loading_constant_turn.index(min(thrust_loading_constant_turn))]]

    # # when there are intersections
    # thrust = []
    # weight = []
    # if len(thrust_intersections) > 0:
    #     thrust += [thrust_intersections, thrust_conditions]
    #     weight += [weight_intersections, weight_conditions]
    #     thrust = [item for sublist in thrust for item in sublist]
    #     weight = [item for sublist in weight for item in sublist]

    #     TW = max(thrust)
    #     optimum_index = thrust.index(TW)
    #     WS = weight[optimum_index]

    # # when there are no intersections
    # else:
    #     TW = max(thrust_conditions)
    #     optimum_index = thrust_conditions.index(TW)
    #     WS = weight_conditions[optimum_index]

    logger.debug(f"{ TW = } { WS = }")

    # Vstall regulated by CS 25.103: not really specified
    # I actually have to calculate the stall speed from the CLmax
    # once optimum point is found we use the value of W/S to calculate the V_stall for the CLmax
    # provided and we can calculate the V_stall from here

    V_stall = np.sqrt(2 / density / C_L_max * WS)

    # save results into the aircraft
    aircraft.thrust_over_weight = TW
    aircraft.weight_over_surface = WS
    # aircraft.clean_stall_speed = V_stall

    return


if __name__ == "__main__":
    get_constraints(1, 2)
