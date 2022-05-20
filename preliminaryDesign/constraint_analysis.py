from cProfile import label
import matplotlib.pyplot as plt
import numpy as np


def main():
    """
    Produce a constraint diagram - W/S vs T/W
    """

    aspect_ratio = 8
    oswald_efficiency = 1.78 * (1 - 0.045 * aspect_ratio ** 0.68) - 0.64
    lift_induced_drag_constant = 1 / (np.pi * aspect_ratio * oswald_efficiency)

    rho_4000m = 0.8194
    velocity = 200
    dynamic_pressure = 0.5 * rho_4000m * velocity ** 2

    max_bank_angle = 30 / 180 * np.pi  # rad
    load_factor = 1 / np.cos(max_bank_angle)

    C_D_min = 0.055

    wing_loading_points = np.linspace(2000, 20000, 1000)

    thrust_loading_cruise = dynamic_pressure * C_D_min / wing_loading_points + \
        lift_induced_drag_constant / dynamic_pressure * wing_loading_points

    plt.plot(wing_loading_points, thrust_loading_cruise,
             'r', label='cruise speed')

    thrust_loading_constant_turn = dynamic_pressure * \
        (C_D_min / wing_loading_points + lift_induced_drag_constant *
         (load_factor / dynamic_pressure) ** 2 * wing_loading_points)

    plt.plot(wing_loading_points, thrust_loading_constant_turn,
             'b', label='constant turn')

    required_climb_rate = 5

    thrust_loading_climb_rate = required_climb_rate / velocity + dynamic_pressure / \
        wing_loading_points * C_D_min + lift_induced_drag_constant / \
        dynamic_pressure * wing_loading_points

    plt.plot(wing_loading_points, thrust_loading_climb_rate,
             'g', label='climb rate')

    plt.xlabel('W/S')
    plt.ylabel('T/W')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
