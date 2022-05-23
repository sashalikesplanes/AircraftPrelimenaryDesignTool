import imp
from Component import Component
from FuselageGroup import FuselageGroup
from WingGroup import WingGroup


class Aircraft(Component):
    def __init__(self):
        super().__init__()
        self.WingGroup = WingGroup(self)
        self.FuselageGroup = FuselageGroup(self)
        self.components += [self.WingGroup, self.FuselageGroup]
