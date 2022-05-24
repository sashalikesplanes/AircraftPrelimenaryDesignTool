# To Check
from detailedDesign.classes.Component import Component


class Engines(Component):
    def __init__(self, WingGroup, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self._freeze()
