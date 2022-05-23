# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.HLDs import HLDs


class Wing(Component):
    def __init__(self, WingGroup):
        super().__init__()
        self.WingGroup = WingGroup
        self.HLDs = HLDs(self)
        self.components += [self.HLDs]
