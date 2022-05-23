from detailedDesign.classes.Component import Component


class CargoBay(Component):
    def __init__(self, Fuselage, config):
        my_config = super().__init__(config)
        self.Fuselage = Fuselage
