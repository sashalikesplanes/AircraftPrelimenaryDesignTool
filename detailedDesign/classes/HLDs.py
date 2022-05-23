# To Check
from detailedDesign.classes.Component import Component


class HLDs(Component):
    def __init__(self, Wing, config):
        my_config = super().__init__(config)
        self.Wing = Wing

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()
