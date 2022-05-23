from detailedDesign.classes.Component import Component


class CargoBay(Component):
    def __init__(self, Fuselage):
        super().__init__()
        self.Fuselage = Fuselage
