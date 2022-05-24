# To check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuelCells import FuelCells
from detailedDesign.classes.Batteries import Batteries


class Power(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)

        self.FuselageGroup = FuselageGroup

        self.FuelCells = FuelCells(self, self.design_config)
        self.Batteries = Batteries(self, self.design_config)
        self.components = [self.FuelCells, self.Batteries]

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        pass
