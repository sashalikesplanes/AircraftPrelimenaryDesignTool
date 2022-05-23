# To check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuelCells import FuelCells
from detailedDesign.classes.Batteries import Batteries


class Power(Component):
    def __init__(self, FuselageGroup):
        super().__init__()
        self.FuselageGroup = FuselageGroup
        self.FuelCells = FuelCells(self)
        self.Batteries = Batteries(self)
        self.components += [self.FuelCells, self.Batteries]
