import numpy as np

from misc.constants import mass_per_passenger


class Passenger:
    def __init__(self, vec3=np.array([0., 0., 0.])):
        self.name = "Hans"
        self.mass = mass_per_passenger
        self.pos = vec3

    def give_seat(self, vec3):
        self.pos = vec3
