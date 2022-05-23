# To check
from detailedDesign.classes.Component import Component


class FuelCells(Component):
    def __init__(self, Power, config):
        my_config = super().__init__(config)
        self.Power = Power
