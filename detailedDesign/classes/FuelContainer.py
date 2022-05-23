from detailedDesign.classes.Component import Component


class FuelContainer(Component):
    def __init__(self, Fuselage, config):
        my_config = super().__init__(config)
        self.Fuselage = Fuselage

        self.RemovableContainers = []
        self.NonRemovableContainers = []
        self.components += self.RemovableContainers + self.NonRemovableContainers

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()


def size_self(self):
    pass
