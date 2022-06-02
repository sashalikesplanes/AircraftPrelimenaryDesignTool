import numpy as np

from detailedDesign.classes.Component import Component


class CargoBay(Component):
    def __init__(self, Fuselage, design_config):
        super().__init__(design_config)

        self.Fuselage = Fuselage

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self.height = None
        self.width = None
        self.current_cargo_mass = 0

        self._freeze()

    def size_self(self):
        # diameter = self.Fuselage.Cabin.diameter
        # height = self.Fuselage.Cabin.height
        # width = self.Fuselage.Cabin.width

        # # print("Hello from CargoBay!")
        # # print(diameter)
        # # print(height, width)

        # if diameter is not None:
        #     # Calculate the cross-sectional area of a rectangle of
        #     # width half diameter which fits under the cabin
        #     w = 0.5 * diameter
        #     x = w / 2
        #     h = (w ** 2 - x ** 2) ** 0.5 - 0.5 * height
        #     S = h * w
        #     # print(h, w, S)
        #     self.height = h
        #     self.width = w

        self.pos = np.array([self.Fuselage.cockpit_length, 0., 0.])

    def get_mass(self):
        mass = self.own_mass + self.current_cargo_mass
        return mass
