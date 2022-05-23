# To check
from Component import Component
from VerticalTail import VerticalTail
from HorizontalTail import HorizontalTail


class Tail(Component):
    def __init__(self, FuselageGroup):
        super.__init__()
        self.FuselageGroup = FuselageGroup
        self.VerticalTail = VerticalTail(self)
        self.HorizontalTail = HorizontalTail(self)
        self.components += [self.VerticalTail , self.HorizontalTail]

