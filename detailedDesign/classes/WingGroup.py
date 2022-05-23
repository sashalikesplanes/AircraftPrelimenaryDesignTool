# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.Wing import Wing
from detailedDesign.classes.Engines import Engines


class WingGroup(Component):
    def __init__(self, Aircraft):
        super().__init__()

        self.Aircraft = Aircraft

        self.Wing = Wing(self)
        self.Engines = Engines(self)
        self.components += [self.Wing, self.Engines]
