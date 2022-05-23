# To Check
from detailedDesign.classes.Component import Component


class Engines(Component):
    def __init__(self, WingGroup):
        super().__init__()
        self.WingGroup = WingGroup
        self.config = self.WingGroup.config["Engines"]
        self.count = 69
        self.engineSpecificPower = self.config["engineSpecificPower"]
