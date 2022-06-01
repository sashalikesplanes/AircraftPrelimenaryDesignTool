import numpy as np
import matplotlib.pyplot as plt

from detailedDesign.classes.Passenger import Passenger


def make_potato_plot(aircraft):
    fig, axs = plt.subplots(2, 2)

    aircraft.get_cged()
    cabin = aircraft.FuselageGroup.Fuselage.Cabin

    length = cabin.length
    width = cabin.width
    height = cabin.height
    n_sa = cabin.seats_abreast
    n_rows = cabin.rows_per_floor
    n_floors = cabin.floor_count
    n_aisle = cabin.aisle_count

    vec_x = np.array([length / n_rows, 0., 0.])
    vec_y_seat = np.array([0., cabin.seat_width, 0.])
    vec_y_aisle = np.array([0., cabin.seat_width + cabin.aisle_width, 0.])
    vec_z = np.array([0., 0., height / n_floors])

    vec_initial = np.array([vec_x[0] / 2, -(width - cabin.seat_width) / 2, -(n_floors - 1) * 0.5 * vec_z[2]])
    # print(vec_x, vec_y_seat, vec_y_aisle, vec_z)

    # Curve 1
    plt_1 = list()
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    for x in range(int(n_rows)):
        for y in range(int(n_sa)):
            for z in range(n_floors):
                # print(x, y, z)
                vec3 = vec_initial + x * vec_x + y * vec_y_seat + vec_z * z
                new_person = Passenger(vec3)
                cabin.passengers.append(new_person)
                cg = aircraft.get_cg()
                plt_1.append((cg, aircraft.get_mass()))
    plot_potato_curve(aircraft, plt_1, axs)

    # Curve 2
    cabin.passengers = []
    plt_1 = list()
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    for x in reversed(range(int(n_rows))):
        for y in reversed(range(int(n_sa))):
            for z in reversed(range(n_floors)):
                # print(x, y, z)
                vec3 = vec_initial + x * vec_x + y * vec_y_seat + vec_z * z
                new_person = Passenger(vec3)
                cabin.passengers.append(new_person)
                cg = aircraft.get_cg()
                plt_1.append((cg, aircraft.get_mass()))
    plot_potato_curve(aircraft, plt_1, axs)

    plt.show()


def plot_potato_curve(aircraft, data, axs):
    """Function to easily plot potato data"""
    lst_x = []
    lst_y = []
    lst_z = []
    lst_mass = []

    for i in data:
        lst_mass.append(i[1])
        lst_x.append(i[0][0])
        lst_y.append(i[0][1])
        lst_z.append(i[0][2])

    lst_x_lemac = [None] * len(lst_x)
    for i in range(len(lst_x)):
        lst_x_lemac[i] = (lst_x[i] - aircraft.x_lemac) / aircraft.WingGroup.Wing.mean_geometric_chord

    axs[0, 0].plot(lst_x_lemac, lst_mass, 'bo-')
    axs[0, 1].plot(lst_x, lst_mass, 'bo-')
    axs[1, 0].plot(lst_y, lst_mass, 'bo-')
    axs[1, 1].plot(lst_z, lst_mass, 'bo-')
