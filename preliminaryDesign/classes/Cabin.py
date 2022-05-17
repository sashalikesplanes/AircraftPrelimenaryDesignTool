import numpy as np


class Cabin:
    def __init__(self, plane):
        n_sa = int(np.ceil(0.45 * plane.passengers ** 0.5))

        # Amount of floors of a maximum of 12 people
        n_floors = int(np.ceil(n_sa / 12))
        n_rows = int(np.ceil(plane.passengers / n_sa))
        # Number of people on the top floor
        n_top = int(n_sa % 12)
        print(n_top, n_rows)

        l_cabin = 1.17 * n_rows
        n_pax = n_sa * n_rows
        print(n_pax, l_cabin)
