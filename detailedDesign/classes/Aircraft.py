from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup
from misc.constants import g


class Aircraft(Component):
    def __init__(self, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup(self, self.design_config)
        self.FuselageGroup = FuselageGroup(self, self.design_config)
        self.components = [self.WingGroup, self.FuselageGroup]

        # Create all the parameters that this component must have here:
        # Use self.property = None
        self.mtom = None
        self.thrust_over_weight = None
        self.weight_over_surface = None
        self.reference_area = None
        self.reference_thrust = None

        self._freeze()

    def size_self(self):
        self.reference_area = self.mtom * g / kwargs['weight_over_surface']
        self.reference_thrust = self.mtom * g * thrust_over_weight
        print(self.reference_area, self.reference_thrust)
