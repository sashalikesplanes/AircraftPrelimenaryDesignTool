# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.Tail import Tail
from detailedDesign.classes.Power import Power
from detailedDesign.classes.Fuselage import Fuselage


class FuselageGroup(Component):
    def __init__(self, Aircraft, config):
        my_config = super().__init__(config)
        self.Aircraft = Aircraft

        self.Tail = Tail(self, my_config)
        self.Power = Power(self, my_config)
        self.Fuselage = Fuselage(self, my_config)
        self.components += [self.Tail, self.Power, self.Fuselage]

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self._freeze()

    def size_self(self):
        pass
