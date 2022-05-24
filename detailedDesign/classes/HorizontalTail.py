# To check
from detailedDesign.classes.Component import Component


class HorizontalTail(Component):
    def __init__(self, Tail, design_config):
        super().__init__(design_config)

        self.Tail = Tail

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()
