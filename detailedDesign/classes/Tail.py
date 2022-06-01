# To check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.VerticalTail import VerticalTail
from detailedDesign.classes.HorizontalTail import HorizontalTail
import numpy as np

class Tail(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)

        self.FuselageGroup = FuselageGroup

        self.VerticalTail = VerticalTail(self, self.design_config)
        self.HorizontalTail = HorizontalTail(self, self.design_config)
        self.components = [self.VerticalTail, self.HorizontalTail]

        # Create all the parameters that this component must have here:
        # Using self.property_name = None

        self._freeze()  # Last line

    def size_self(self):
        self.pos = np.array([self.FuselageGroup.Fuselage.length, 0., -self.FuselageGroup.Fuselage.outer_diameter/2])

    def get_sized(self):
        for component in self.components:
            component.get_sized()
        self.size_self()
