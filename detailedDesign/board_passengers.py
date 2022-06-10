import numpy as np

from detailedDesign.classes.Passenger import Passenger

def unboard_passengers_fuel(aircraft):
    aircraft.FuselageGroup.Fuselage.Cabin.passengers = []
    fuselage.AftFuelContainer.current_fuel_mass = 0
    fuselage.AssFuelContainer.current_fuel_mass = 0
    fuselage.ForwardFuelContainer.current_fuel_mass = 0

    return aircraft

def board_passengers_half_fuel(aircraft):
    board_passengers(aircraft)
    fuselage.AftFuelContainer.current_fuel_mass = fuselage.AftFuelContainer.mass_H2 / 2
    fuselage.AssFuelContainer.current_fuel_mass = fuselage.AssFuelContainer.mass_H2 / 2
    fuselage.ForwardFuelContainer.current_fuel_mass = fuselage.ForwardFuelContainer.mass_H2 / 2



def board_passengers(aircraft):
    aircraft.get_cged()
    cabin = aircraft.FuselageGroup.Fuselage.Cabin

    length = cabin.length
    width = cabin.width
    height = cabin.height
    n_sa = cabin.seats_abreast
    n_rows = cabin.rows_per_floor
    n_floors = cabin.floor_count
    n_aisle = cabin.aisle_count

    # Find isle locations
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

    # Vectors pointing to different positions
    vec_x = np.array([length / n_rows, 0., 0.])
    vec_y_seat = np.array([0., cabin.seat_width, 0.])
    vec_y_aisle = np.array([0., cabin.aisle_width, 0.])
    vec_z = np.array([0., 0., height / n_floors])

    vec_initial = np.array([vec_x[0] / 2, -(width - cabin.seat_width) / 2, -(n_floors - 1) * 0.5 * vec_z[2]])

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

    fuselage = aircraft.FuselageGroup.Fuselage
    # Board the fuel
    fuselage.AftFuelContainer.current_fuel_mass = fuselage.AftFuelContainer.mass_H2
    fuselage.AssFuelContainer.current_fuel_mass = fuselage.AssFuelContainer.mass_H2
    fuselage.ForwardFuelContainer.current_fuel_mass = fuselage.ForwardFuelContainer.mass_H2

    return aircraft
