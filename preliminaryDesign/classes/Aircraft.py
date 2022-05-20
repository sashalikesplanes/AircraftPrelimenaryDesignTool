import numpy as np

from misc.openData import openData
from preliminaryDesign.classes.Fuselage import Fuselage
from preliminaryDesign.classes.Wing import Wing


class Aircraft:
    def __init__(self, file):
        data = openData(file)

        # Cargo related data
        self.passengers = data["passengers"]
        self.cargoMass = data["cargoMass"]
        self.passengerMass = data["passengerMass"]

        # Components
        self.fuselage = None
        self.wing = None
        self.tail = None

    def makeFuselage(self):
        self.fuselage = Fuselage()
        self.fuselage.designCabin(self)

    def makeWing(self):
        self.wing = Wing()
