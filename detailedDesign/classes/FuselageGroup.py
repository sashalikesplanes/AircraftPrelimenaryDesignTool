# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.Tail import Tail
from detailedDesign.classes.Power import Power


class FuselageGroup(Component):
    def __init__(self, Aircraft):
        super().__init__()
        self.Aircraft = Aircraft
        self.Tail = Tail(self)
        self.Power = Power(self)
        self.components += [self.Tail, self.Power]
