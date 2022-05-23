# To check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.VerticalTail import VerticalTail
from detailedDesign.classes.HorizontalTail import HorizontalTail


class Tail(Component):
    def __init__(self, FuselageGroup):
        super.__init__()
        self.FuselageGroup = FuselageGroup
        self.VerticalTail = VerticalTail(self)
        self.HorizontalTail = HorizontalTail(self)
        self.components += [self.VerticalTail , self.HorizontalTail]

