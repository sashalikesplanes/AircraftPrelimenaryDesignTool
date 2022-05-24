import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_constraints(aircraft):
    """
    Produce a constraint diagram - W/S vs T/W
    """

    #Parameters needed
    aspect_ratio = aircraft.WingGroup.Wing.AspectRatio
    oswald_efficiency = 1.78 * (1 - 0.045 * aspect_ratio ** 0.68) - 0.64
    lift_induced_drag_constant = 1 / (np.pi * aspect_ratio * oswald_efficiency)

    velocity = aircraft.states['cruise'].velocity
    density = aircraft.states['cruise'].density
    dynamic_pressure = 0.5 * density * velocity ** 2

    max_bank_angle = 40 / 180 * np.pi  # rad   #taken from regulation
    load_factor = 1 / np.cos(max_bank_angle)

    C_D_min = aircraft.C_D_min  
    C_L_max = aircraft.C_L_max  
    required_climb_rate = 10  # from regulation I believe but I cannot find anything about it
    #therefore we take ot from the yamel and it is something we change in order to make it work

    #Start calculating the functions
    wing_loading_points = np.linspace(2000, 100000, 1000)

    # q using turning speed and associated altitude
    thrust_loading_constant_turn = dynamic_pressure * \
        (C_D_min / wing_loading_points + lift_induced_drag_constant *
         (load_factor / dynamic_pressure) ** 2 * wing_loading_points)

    # q using climb airspeed and associated altitude
    thrust_loading_climb_rate = required_climb_rate / velocity + dynamic_pressure / \
        wing_loading_points * C_D_min + lift_induced_drag_constant / \
        dynamic_pressure * wing_loading_points

    thrust_loading_cruise = dynamic_pressure * C_D_min / wing_loading_points + \
        lift_induced_drag_constant / dynamic_pressure * wing_loading_points

    #Plot the fuctions
    fig, ax = plt.subplots()

    ax.plot(wing_loading_points, thrust_loading_cruise,
            'r', label='Cruise speed')

    ax.plot(wing_loading_points, thrust_loading_constant_turn,
            'b', label='Constant turn')

    ax.plot(wing_loading_points, thrust_loading_climb_rate,
            'g', label='Climb rate')

    ax.set_xlabel('W/S')
    ax.set_ylabel('T/W')

    plt.legend()

    plt.show()

    #Calculate optimum
        #If they do not intersect
            #Calculate min of each
            #Optimum is the max of those
        #If they intersect
            #Calculate where they intersect
            #Calculate min of each
            #Optimum is the max of those

    # calculate intersections
    thrust_intersections = []
    weight_intersections = []
    idx1 = np.argwhere(np.diff(np.sign(thrust_loading_cruise - thrust_loading_climb_rate))).flatten()
    idx2 = np.argwhere(np.diff(np.sign(thrust_loading_cruise - thrust_loading_constant_turn))).flatten()
    idx3 = np.argwhere(np.diff(np.sign(thrust_loading_climb_rate - thrust_loading_constant_turn))).flatten()

    thrust_intersections += [thrust_loading_cruise[idx1], thrust_loading_cruise[idx2], thrust_loading_climb_rate[idx3]]
    thrust_intersections = list(filter(None, thrust_intersections))
    weight_intersections += [wing_loading_points[idx1], wing_loading_points[idx2], wing_loading_points[idx3]]
    weight_intersections = list(filter(None, weight_intersections))
    thrust_intersections = [i[0] for i in thrust_intersections]
    weight_intersections = [i[0] for i in weight_intersections]

    #calculate minimum of each curve
    thrust_conditions = []  
    weight_conditions = []
    thrust_loading_cruise = thrust_loading_cruise.tolist()
    thrust_loading_climb_rate = thrust_loading_climb_rate.tolist()
    thrust_loading_constant_turn = thrust_loading_constant_turn.tolist()
    thrust_conditions += [min(thrust_loading_cruise), min(thrust_loading_climb_rate), min(thrust_loading_constant_turn)]
    weight_conditions += [wing_loading_points[thrust_loading_cruise.index(min(thrust_loading_cruise))], wing_loading_points[thrust_loading_climb_rate.index(min(thrust_loading_climb_rate))], \
        wing_loading_points[thrust_loading_constant_turn.index(min(thrust_loading_constant_turn))]]

    #when there are intersections
    thrust = []
    weight = []
    if len(thrust_intersections) > 0:
        thrust += [thrust_intersections, thrust_conditions]
        weight += [weight_intersections, weight_conditions]
        thrust = [item for sublist in thrust for item in sublist]
        weight = [item for sublist in weight for item in sublist]

        TW = max(thrust)
        optimum_index = thrust.index(TW)
        WS = weight[optimum_index]

    #when there are no intersections
    else:
        TW = max(thrust_conditions)
        optimum_index = thrust_conditions.index(TW)
        WS = weight_conditions[optimum_index]
    
    print(TW, WS)

    # Vstall regulated by CS 25.103: not really specified
    # I actually have to calculate the stall speed from the CLmax
    #once optimum point is found we use the value of W/S to calculate the V_stall for the CLmax
    #provided and we can calculate the V_stall from here

    V_stall = np.sqrt(2 / density / C_L_max * WS)
    
    #save results into the aircraft
    aircraft.thrust_over_weight = TW
    aircraft.weight_over_surface = WS
    #save stall speed

    return 

if __name__ == "__main__":
    get_constraints(1, 2)
