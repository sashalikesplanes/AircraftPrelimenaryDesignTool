# To check
from detailedDesign.classes.Component import Component


class FuelCells(Component):
    def __init__(self, Power, design_config):
        super().__init__(design_config)

        self.Power = Power

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()
