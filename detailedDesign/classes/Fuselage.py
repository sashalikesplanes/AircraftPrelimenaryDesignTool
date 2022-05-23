from detailedDesign.classes.Component import Component
from detailedDesign.classes.Cabin import Cabin
from detailedDesign.classes.FuelContainer import FuelContainer
from detailedDesign.classes.CargoBay import CargoBay


class Fuselage(Component):
    def __int__(self, FuselageGroup):
        super().__init__()
        self.FuselageGroup = FuselageGroup

        self.CargoBay = CargoBay(self)
        self.Cabin = Cabin(self)
        self.FuelContainer = FuelContainer(self)
        self.components += [self.CargoBay, self.Cabin, self.FuelContainer]
