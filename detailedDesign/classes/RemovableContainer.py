from detailedDesign.classes.Component import Component


class RemovableContainer(Component):
    def __init__(self, FuelContainer, config):
        my_config = super().__init__(config)
        self.FuelContainer = FuelContainer
