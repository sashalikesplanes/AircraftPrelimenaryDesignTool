# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.HLDs import HLDs


class Wing(Component):
    def __init__(self, WingGroup, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup
        self.HLDs = HLDs(self, self.design_config)
        self.components = [self.HLDs]

        # Create all the parameters that this component must have here:
        # Using self.property_name = None
        self._freeze()
