from detailedDesign.classes.Component import Component


class RemovableContainer(Component):
    def __init__(self, FuelContainer, design_config):
        super().__init__(design_config)
        self.FuelContainer = FuelContainer

        # Create all the parameters that this component must have here:
        # Using self.property_name = None

        self._freeze()  # Last line
