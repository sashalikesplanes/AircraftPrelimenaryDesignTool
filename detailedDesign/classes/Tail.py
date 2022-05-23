# To check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.VerticalTail import VerticalTail
from detailedDesign.classes.HorizontalTail import HorizontalTail


class Tail(Component):
    def __init__(self, FuselageGroup, config):
        my_config = super().__init__(config)
        self.FuselageGroup = FuselageGroup
        self.VerticalTail = VerticalTail(self, my_config)
        self.HorizontalTail = HorizontalTail(self, my_config)
        self.components += [self.VerticalTail, self.HorizontalTail]

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        pass
