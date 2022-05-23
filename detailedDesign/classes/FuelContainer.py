from detailedDesign.classes.Component import Component


class FuelContainer(Component):
    def __init__(self, Fuselage):
        super().__init__()
        self.Fuselage = Fuselage

        self.RemovableContainers = []
        self.NonRemovableContainers = []
        self.components += self.RemovableContainers + self.NonRemovableContainers
