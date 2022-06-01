# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.Wing import Wing
from detailedDesign.classes.Engines import Engines
import numpy as np

class WingGroup(Component):
    def __init__(self, Aircraft, design_config):
        super().__init__(design_config)

        self.Aircraft = Aircraft

        self.Wing = Wing(self, self.design_config)
        self.Engines = Engines(self, self.design_config)
        self.components = [self.Wing, self.Engines]

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def get_sized(self):
        for component in self.components:
            component.get_sized()

            self.logger.debug(f"Mass of {type(component).__name__} : {component.get_mass():.4E} kg")
        self.size_self()

    def size_self(self):
        self.pos = np.array([self.Aircraft.x_lemac, 0., -self.Aircraft.FuselageGroup.Fuselage.outer_diameter/2])