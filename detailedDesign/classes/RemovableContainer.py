from detailedDesign.classes.Component import Component


class RemovableContainer(Component):
    def __init__(self, FuelContainer, config):
        my_config = super().__init__(config)
        self.FuelContainer = FuelContainer

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()
