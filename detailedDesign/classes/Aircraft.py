from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup


class Aircraft(Component):
    def __init__(self):
        super().__init__()
        self.WingGroup = WingGroup(self)
        self.FuselageGroup = FuselageGroup(self)
        self.components += [self.WingGroup, self.FuselageGroup]
