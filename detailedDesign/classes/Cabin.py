from detailedDesign.classes.Component import Component


class Cabin(Component):
    def __int__(self, Fuselage):
        super().__init__()
        self.Fuselage = Fuselage
