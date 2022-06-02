import numpy as np

from misc.constants import mass_per_passenger, cargo_cabin_fraction


class Passenger:
    def __init__(self, vec3=np.array([0., 0., 0.])):
        self.name = "Hans"
        self.mass = mass_per_passenger * cargo_cabin_fraction
        self.pos = vec3

    def give_seat(self, vec3):
        self.pos = vec3
