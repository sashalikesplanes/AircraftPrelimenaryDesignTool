from detailedDesign.classes.Component import Component


class FuelContainer(Component):
    def __init__(self, Fuselage, design_config):
        super().__init__(design_config)

        self.Fuselage = Fuselage

        self.RemovableContainers = []
        self.NonRemovableContainers = []
        self.components = self.RemovableContainers + self.NonRemovableContainers

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self.thickness = 0
        self.inner_diameter = None
        self._freeze()

    def size_self(self):
        self.Fuselage.inner_diameter

        self.inner_diameter = self.Fuselage.inner_diameter - self.thickness * 2
        self.thickness = 1
