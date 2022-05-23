import imp
from Component import Component
from FuselageGroup import FuselageGroup


class Aircraft(Component):
    def __init__(self):
        super().__init__()
        self.WingGroup = None
        self.FuselageGroup = FuselageGroup(self)
        self.components += [self.WingGroup, self.FuselageGroup]
