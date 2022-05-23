# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.HLDs import HLDs


class Wing(Component):
    def __init__(self, WingGroup, config):
        my_config = super().__init__(config)
        self.WingGroup = WingGroup
        self.HLDs = HLDs(self, my_config)
        self.components += [self.HLDs]

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()
