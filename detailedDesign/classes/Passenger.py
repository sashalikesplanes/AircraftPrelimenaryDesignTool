import numpy as np

from misc.constants import mass_per_passenger


class Passenger:
    def __init__(self):
        self.name = "Hans"
        self.mass = mass_per_passenger
        self.pos = np.array([0., 0., 0.])

    def give_seat(self):
        print(f"I ({self.name}) don't have a seat. :-(")
