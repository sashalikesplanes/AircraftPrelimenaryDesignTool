from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup


class Aircraft(Component):
    def __init__(self, config):
        super().__init__()
        print(config)

        self.WingGroup = WingGroup(self)
        self.FuselageGroup = FuselageGroup(self, config["FuselageGroup"])
        self.components += [self.WingGroup, self.FuselageGroup]
