import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from detailedDesign.classes.Passenger import Passenger
from misc.constants import mass_per_passenger, cargo_cabin_fraction
from detailedDesign.classes.Aircraft import Aircraft


def make_carrot_plot(aircraft):
    max_length = aircraft.FuselageGroup.Fuselage.length
    x_lemacs = np.arange(0, max_length)

    for x_lemac in x_lemacs:
        config_file = Path('data', 'new_designs', 'config.yaml')
        aircraft = Aircraft(config_file, aircraft.states, debug=False)
        aircraft.x_lemac = x_lemac



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

    cuts = []
    if n_aisle == 1:
        cut_1 = np.ceil(n_sa / 2) - 1
        cuts = [cut_1]
    elif n_aisle == 2:
        cut_1 = 2
        cut_2 = n_sa - 3
        cuts = [cut_1, cut_2]
    elif n_aisle == 3:
        cut_1 = 2
        cut_2 = n_sa - 3
        cut_3 = np.ceil(n_sa / 2) - 1
        cuts = [cut_1, cut_2, cut_3]
    elif n_aisle == 4:
        cut_1 = 2
        cut_2 = n_sa - 3
        cut_middle = np.ceil(n_sa / 2) - 1
        cut_3 = cut_middle + 2
        cut_4 = cut_middle - 2
        cuts = [cut_1, cut_2, cut_3, cut_4]
    else:
        # print(n_aisle)
        # print(n_sa)
        raise ValueError

    vec_x = np.array([length / n_rows, 0., 0.])
    vec_y_seat = np.array([0., cabin.seat_width, 0.])
    vec_y_aisle = np.array([0., cabin.aisle_width, 0.])
    vec_z = np.array([0., 0., height / n_floors])

    vec_initial = np.array([vec_x[0] / 2, -(width - cabin.seat_width) / 2, -(n_floors - 1) * 0.5 * vec_z[2]])
    # print(vec_x, vec_y_seat, vec_y_aisle, vec_z)

    # Save all results to find cg range in x
    plt_2 = list()

    # Cargo stuff
    cargo_place = aircraft.FuselageGroup.Fuselage.CargoBay
    plt_1 = list()
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    n_pax = n_sa * n_rows * n_floors
    cargo_mass = n_pax * mass_per_passenger * (1 - cargo_cabin_fraction)
    cargo_place.current_cargo_mass = cargo_mass
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    plot_potato_curve(aircraft, plt_1, axs, c="b")
    plt_2 += plt_1

    # Y-Spud 1
    cabin.passengers = []
    plt_1 = list()
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    for y_value in range(int(n_sa)):
        if y_value % 2:
            continue
        for x in range(int(n_rows)):
            for z in range(n_floors):
                # print(x, y_value, z)
                for y in [y_value, y_value + 1]:
                    # print(n_sa - 1, y_value + 1)
                    if n_sa <= y_value + 1:
                        pass
                    else:
                        n_cuts = 0
                        for cut in cuts:
                            if cut < y:
                                n_cuts += 1

                        vec3 = vec_initial + x * vec_x + y * vec_y_seat + vec_z * z + n_cuts * vec_y_aisle
                        new_person = Passenger(vec3)
                        cabin.passengers.append(new_person)
                        cg = aircraft.get_cg()
                        plt_1.append((cg, aircraft.get_mass()))
    plot_potato_curve(aircraft, plt_1, axs, c="r")
    plt_2 += plt_1

    # Y-Spud 2
    cabin.passengers = []
    plt_1 = list()
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    for y_value in reversed(range(int(n_sa))):
        if y_value % 2:
            continue
        for x in reversed(range(int(n_rows))):
            for z in reversed(range(n_floors)):
                # print(x, y_value, z)
                for y in [y_value, y_value + 1]:
                    # print(n_sa - 1, y_value + 1)
                    if n_sa <= y_value + 1:
                        pass
                    else:
                        n_cuts = 0
                        for cut in cuts:
                            if cut < y:
                                n_cuts += 1

                        vec3 = vec_initial + x * vec_x + y * vec_y_seat + vec_z * z + n_cuts * vec_y_aisle
                        new_person = Passenger(vec3)
                        cabin.passengers.append(new_person)
                        cg = aircraft.get_cg()
                        plt_1.append((cg, aircraft.get_mass()))
    plot_potato_curve(aircraft, plt_1, axs, c="r")
    plt_2 += plt_1

    # Z-Spud 1
    cabin.passengers = []
    plt_1 = list()
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    for z in range(n_floors):
        for y in range(int(n_sa)):
            for x in range(int(n_rows)):
                # print(x, y, z)
                n_cuts = 0
                for cut in cuts:
                    if cut < y:
                        n_cuts += 1

                vec3 = vec_initial + x * vec_x + y * vec_y_seat + vec_z * z + n_cuts * vec_y_aisle
                new_person = Passenger(vec3)
                cabin.passengers.append(new_person)
                cg = aircraft.get_cg()
                plt_1.append((cg, aircraft.get_mass()))
    plot_potato_curve(aircraft, plt_1, axs, c="g")
    plt_2 += plt_1

    # Z-Spud 2
    cabin.passengers = []
    plt_1 = list()
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    for z in reversed(range(n_floors)):
        for y in reversed(range(int(n_sa))):
            for x in reversed(range(int(n_rows))):
                # print(x, y, z)
                n_cuts = 0
                for cut in cuts:
                    if cut < y:
                        n_cuts += 1

                vec3 = vec_initial + x * vec_x + y * vec_y_seat + vec_z * z + n_cuts * vec_y_aisle
                new_person = Passenger(vec3)
                cabin.passengers.append(new_person)
                cg = aircraft.get_cg()
                plt_1.append((cg, aircraft.get_mass()))
    plot_potato_curve(aircraft, plt_1, axs, c="g")
    plt_2 += plt_1

    # Fuel stuff
    fuel_storage = aircraft.FuselageGroup.Fuselage.FuelContainer
    plt_1 = list()
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    max_fuel_mass = fuel_storage.mass_H2
    fuel_storage.current_fuel_mass = max_fuel_mass
    plt_1.append((aircraft.get_cg(), aircraft.get_mass()))
    plot_potato_curve(aircraft, plt_1, axs, c="b")
    plt_2 += plt_1

    cg_range = find_cg_range(plt_2, aircraft)
    print(cg_range)

    plt.show()


def plot_potato_curve(aircraft, data, axs, c="b"):
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
    dots = ""

    axs[0, 0].plot(lst_x_lemac, lst_mass, f'{c}{dots}-')
    axs[0, 0].set_title("X cg loading diagram")
    axs[0, 0].set(xlabel='X [% mac]', ylabel='Total Mass [kg]')

    axs[0, 1].plot(lst_x, lst_mass, f'{c}{dots}-')
    axs[0, 1].set_title("X cg loading diagram")
    axs[0, 1].set(xlabel='X [m]', ylabel='Total Mass [kg]')

    axs[1, 0].plot(lst_y, lst_mass, f'{c}{dots}-')
    axs[1, 0].set_title("Y cg loading diagram")
    axs[1, 0].set(xlabel='Y [m]', ylabel='Total Mass [kg]')

    axs[1, 1].plot(lst_z, lst_mass, f'{c}{dots}-')
    axs[1, 1].set_title("Z cg loading diagram")
    axs[1, 1].set(xlabel='Z [m]', ylabel='Total Mass [kg]')


def find_cg_range(data, aircraft):
    lst_x = []
    for p in data:
        lst_x.append(p[0][0])

    lst_x_lemac = [None] * len(lst_x)
    for i in range(len(lst_x)):
        lst_x_lemac[i] = (lst_x[i] - aircraft.x_lemac) / aircraft.WingGroup.Wing.mean_geometric_chord

    output = (min(lst_x_lemac), max(lst_x_lemac))
    return output
