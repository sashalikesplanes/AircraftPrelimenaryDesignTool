<<<<<<< HEAD
from Component import Component
from Tail import Tail
from Power import Power
=======
# To Check
from detailedDesign.classes.Component import Component

>>>>>>> d0ec95eb6639f204495a1bde9907d2436e8a906e

class FuselageGroup(Component):
    def __init__(self, Aircraft):
        super().__init__()
        self.Aircraft = Aircraft
        self.Tail = Tail(self)
        self.Power = Power(self)
        self.components += [self.Tail, self.Power]