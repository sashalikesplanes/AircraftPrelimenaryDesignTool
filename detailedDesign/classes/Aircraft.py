from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup


class Aircraft(Component):
    def __init__(self, config):
        my_config = super().__init__(config)

        self.WingGroup = WingGroup(self, my_config)
        self.FuselageGroup = FuselageGroup(self, my_config)
        self.components = [self.WingGroup, self.FuselageGroup]

    def size_self(self):
        pass
