from detailedDesign.classes.FuelContainer import FuelContainer
import numpy as np
import matplotlib.pyplot as plt


class ForwardFuelContainer(FuelContainer):
    def __init__(self, Fuselage, design_config):
        super().__init__(Fuselage, design_config)

    def size_self(self):
        super().size_self()

        self.length = self.Fuselage.FuselageGroup.Aircraft.x_lemac - self.Fuselage.cockpit_length

        self.volume_tank = 4 / 3 * np.pi * self.inner_radius ** 3 + np.pi * self.inner_radius ** 2 * self.length

        self.mass_H2 = self.volume_tank * self.density_H2 / (1 + self.Vi)

        self.pos = np.array([self.Fuselage.cockpit_length, 0.,     self.z_offset])

        self.weight_self()
