from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup


class Aircraft(Component):
    def __init__(self, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup(self, self.design_config)
        self.FuselageGroup = FuselageGroup(self, self.design_config)
        self.components = [self.WingGroup, self.FuselageGroup]

        # Create all the parameters that this component must have here:
        # Use self.property = None
        self.mtow = None

        self._freeze()

    def size_self(self):
        pass
