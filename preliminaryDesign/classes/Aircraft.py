import numpy as np

from misc.openData import openData
from preliminaryDesign.classes.Fuselage import Fuselage


class Aircraft:
    def __init__(self, file):
        data = openData(file)

        # Cargo related data
        self.passengers = data["passengers"]
        self.cargoMass = data["cargoMass"]
        self.passengerMass = data["passengerMass"]

        # Components
        self.fuselage = None

    def makeFuselage(self):
        self.fuselage = Fuselage()
        self.fuselage.designCabin(self)
