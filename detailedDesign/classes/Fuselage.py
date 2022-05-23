import numpy as np

from detailedDesign.classes.Component import Component
from detailedDesign.classes.Cabin import Cabin
from detailedDesign.classes.FuelContainer import FuelContainer
from detailedDesign.classes.CargoBay import CargoBay


class Fuselage(Component):
    def __init__(self, FuselageGroup, config):
        my_config = super().__init__(config)
        self.FuselageGroup = FuselageGroup

        self.CargoBay = CargoBay(self, my_config)
        self.Cabin = Cabin(self, my_config)
        self.FuelContainer = FuelContainer(self, my_config)
        self.components = [self.CargoBay, self.Cabin, self.FuelContainer]
        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        # Dimensions
        self.diameter = None

        self._freeze()

    def size_self(self):
        self.diameter = 1.045 * self.Cabin.diameter + 0.084

        if self.CargoBay.width is not None:
            S_cabin = self.Cabin.width * self.Cabin.height
            S_cargo = self.CargoBay.width * self.CargoBay.height

            # Print dead space inside the fuselage
            # print(np.pi * self.diameter ** 2 / 4 - S_cargo - S_cabin)
