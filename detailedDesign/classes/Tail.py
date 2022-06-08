# To check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.VerticalTail import VerticalTail
from detailedDesign.classes.HorizontalTail import HorizontalTail
import numpy as np

class Tail(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)

        self.FuselageGroup = FuselageGroup
        self.parent = self.FuselageGroup

        self.HorizontalTail = HorizontalTail(self, self.design_config)
        self.VerticalTail = VerticalTail(self, self.design_config)
        
        self.components = [self.HorizontalTail, self.VerticalTail]

        # Create all the parameters that this component must have here:
        # Using self.property_name = None

        self._freeze()  # Last line

    def size_self(self):
        self.pos = np.array([self.FuselageGroup.Fuselage.length, 0., -self.FuselageGroup.Fuselage.outer_height/2])

    def get_sized(self):
        for component in self.components:
            component.get_sized()
        self.size_self()

    @property
    def total_mass(self):
        return self.VerticalTail.own_mass + self.HorizontalTail.own_mass
