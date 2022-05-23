from detailedDesign.classes.Component import Component


class RemovableContainer(Component):
    def __init__(self, FuelContainer):
        super().__init__()
        self.FuelContainer = FuelContainer
