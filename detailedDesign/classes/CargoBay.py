from detailedDesign.classes.Component import Component


class CargoBay(Component):
    def __init__(self, Fuselage, config):
        my_config = super().__init__(config)
        self.Fuselage = Fuselage
        self.config = my_config

        self.height = None
        self.width = None

    def size_self(self):
        diameter = self.Fuselage.Cabin.diameter
        height = self.Fuselage.Cabin.height
        width = self.Fuselage.Cabin.width

        # print("Hello from CargoBay!")
        # print(diameter)
        # print(height, width)

        if diameter is not None:
            # Calculate the cross-sectional area of a rectangle of
            # width half diameter which fits under the cabin
            w = 0.5 * diameter
            x = w / 2
            h = (w ** 2 - x ** 2) ** 0.5 - 0.5 * height
            S = h * w
            # print(h, w, S)
            self.height = h
            self.width = w
