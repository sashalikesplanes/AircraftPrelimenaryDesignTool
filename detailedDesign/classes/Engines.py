# To Check
from detailedDesign.classes.Component import Component


class Engines(Component):
    def __init__(self, WingGroup):
        super().__init__()
        self.WingGroup = WingGroup
        self.count = 69
