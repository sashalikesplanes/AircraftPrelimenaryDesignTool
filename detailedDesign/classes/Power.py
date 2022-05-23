# To check
from Component import Component
from FuelCells import FuelCells
from Batteries import Batteries


class Power(Component):
    def __init__(self, FuselageGroup):
        super().__init__()
        self.FuselageGroup = FuselageGroup
        self.FuelCells = FuelCells(self)
        self.Batteries = Batteries(self)
        self.components += [self.FuelCells, self.Batteries]
