#To check
from detailedDesign.classes.Component import Component


class FuelCells(Component):
    def __init__(self, Power):
        super().__init__()
        self.Power = Power