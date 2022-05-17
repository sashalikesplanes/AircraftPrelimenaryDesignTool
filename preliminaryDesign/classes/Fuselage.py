import numpy as np

from preliminaryDesign.classes.Cabin import Cabin


class Fuselage:
    def __init__(self):
        self.cabin = None

    def designCabin(self, plane):
        self.cabin = Cabin(plane)

