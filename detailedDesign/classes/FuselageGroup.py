# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.Tail import Tail
from detailedDesign.classes.Power import Power
from detailedDesign.classes.Fuselage import Fuselage
from detailedDesign.classes.Miscellaneous import Miscellaneous


class FuselageGroup(Component):
    def __init__(self, Aircraft, design_config):
        super().__init__(design_config)

        self.Aircraft = Aircraft

        self.Tail = Tail(self, self.design_config)
        self.Power = Power(self, self.design_config)
        self.Fuselage = Fuselage(self, self.design_config)
        self.Miscellaneous = Miscellaneous(self, self.design_config)

        self.components = [self.Tail, self.Power,
                           self.Fuselage, self.Miscellaneous]

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self._freeze()

    def get_sized(self):
        for component in self.components:
            component.get_sized()

        self.own_mass = self.get_mass()
