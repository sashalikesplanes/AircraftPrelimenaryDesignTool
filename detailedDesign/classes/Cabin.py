from detailedDesign.classes.Component import Component


class Cabin(Component):
    def __init__(self, Fuselage, config):
        my_config = super().__init__(config)
        self.Fuselage = Fuselage
        self.config = my_config

    def size_self(self):
        # Do stuff
        print(self.config)
