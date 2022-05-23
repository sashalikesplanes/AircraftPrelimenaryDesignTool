# To Check
from detailedDesign.classes.Component import Component


class FuselageGroup(Component):
    def __init__(self, Aircraft):
        super().__init__()
        self.Aircraft = Aircraft
