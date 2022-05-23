from Component import Component
from Tail import Tail
from Power import Power

class FuselageGroup(Component):
    def __init__(self, Aircraft):
        super().__init__()
        self.Aircraft = Aircraft
        self.Tail = Tail(self)
        self.Power = Power(self)
        self.components += [self.Tail, self.Power]