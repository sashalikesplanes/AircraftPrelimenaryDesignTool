from detailedDesign.classes.Component import Component
from detailedDesign.classes.Cabin import Cabin


class Fuselage(Component):
    def __int__(self, FuselageGroup):
        super().__init__()
        self.FuselageGroup = FuselageGroup

        self.CargoBay = None
        self.Cabin = Cabin()
        self.FuelContainer = None
