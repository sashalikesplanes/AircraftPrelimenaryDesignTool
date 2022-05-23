from detailedDesign.classes.Component import Component


class FuelContainer(Component):
    def __init__(self, Fuselage, config):
        my_config = super().__init__(config)
        self.Fuselage = Fuselage

        self.RemovableContainers = []
        self.NonRemovableContainers = []
        self.components += self.RemovableContainers + self.NonRemovableContainers
