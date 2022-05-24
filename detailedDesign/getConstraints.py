import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_constraints(aircraft, state):
    """
    Produce a constraint diagram - W/S vs T/W
    """
    #aspect_ratio = aircraft.WingGroup.Wing.AspectRatio
    aspect_ratio = 8
    # might change depending on how we calculate e
    oswald_efficiency = 1.78 * (1 - 0.045 * aspect_ratio ** 0.68) - 0.64
    lift_induced_drag_constant = 1 / (np.pi * aspect_ratio * oswald_efficiency)

    velocity = 200
    density = 0.809
    dynamic_pressure = 0.5 * density * velocity ** 2

    max_bank_angle = 30 / 180 * np.pi  # rad   #from regulation
    load_factor = 1 / np.cos(max_bank_angle)

    C_D_min = 0.055  # will have to be changed in order to account for it iteratively changing
    C_L_max = 1.8  # will have to be changed in order to account for it iteratively changing
    required_climb_rate = 20  # from regulation I believe

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

    # Vstall regulated by CS 25.103
    # I actually have to calculate the stall speed from the CLmax

    V_stall = np.sqrt(2 / density / C_L_max * wing_loading_points)

    ax2 = ax.twinx()

    ax2.plot(wing_loading_points, V_stall, 'y', label=f"At CL_max = {C_L_max}")
    ax2.set_ylabel('Stall Speed')

    plt.legend()
    plt.show()

    # calculate intersections: choose point with minimum
    intersections = []
    values = []
    i = 2000
    while i < 100000:
        if thrust_loading_cruise[i] == V_stall[i]:
            intersections.append(i)
            values.append(thrust_loading_cruise[i])
            i += 1
        elif thrust_loading_climb_rate[i] == V_stall[i]:
            intersections.append(i)
            values.append(thrust_loading_climb_rate[i])
            i += 1
        elif thrust_loading_constant_turn[i] == V_stall[i]:
            intersections.append(i)
            values.append(thrust_loading_constant_turn[i])
            i += 1
        else:
            i += 1

    max_value = max(values)
    max_index = values.index(max_value)
    optimum = intersections[max_index]

<<<<<<< HEAD
    # still have to compute T and S
    return


if __name__ == "__main__":
    get_constraints(1, 2)
=======
    #still have to compute T and S
    return optimum


if __name__ == "__main__":
    get_constraints(1,2)
>>>>>>> b9d0939bf649f01a73862dbf2c454c84ac75cc14
