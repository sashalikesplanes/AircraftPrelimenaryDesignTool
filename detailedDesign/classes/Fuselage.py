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
        self.components += [self.CargoBay, self.Cabin, self.FuelContainer]
