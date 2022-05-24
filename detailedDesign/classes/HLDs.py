# To Check
from detailedDesign.classes.Component import Component


class HLDs(Component):
    def __init__(self, Wing, design_config):
        super().__init__(design_config)
        self.Wing = Wing

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()
