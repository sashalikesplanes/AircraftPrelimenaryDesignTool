# To check
from detailedDesign.classes.Component import Component


class HorizontalTail(Component):
    def __init__(self, Tail, config):
        my_config = super().__init__(config)
        self.Tail = Tail

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()
