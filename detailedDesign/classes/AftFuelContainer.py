from detailedDesign.classes.FuelContainer import FuelContainer
import numpy as np
import matplotlib.pyplot as plt


class AftFuelContainer(FuelContainer):
    def __init__(self, Fuselage, design_config):
        super().__init__(Fuselage, design_config)

    def size_self(self):
        super().size_self()

        self.mass_H2 = self.Fuselage.FuselageGroup.Power.mass_H2 - self.Fuselage.ForwardFuelContainer.mass_H2
        self.volume_tank = self.mass_H2 / self.density_H2 * (1 + self.Vi)

        self.length = (self.volume_tank - 4 / 3 * np.pi * self.inner_radius ** 3) / (np.pi * self.inner_radius ** 2)

        if self.length < 0:
              self.length = 0
              self.radius_tank = (self.volume_tank * 3 / 4 / np.pi) ** (1 / 3)

        self.pos = np.array([self.Fuselage.FuselageGroup.Aircraft.x_lemac + self.Fuselage.FuselageGroup.Aircraft.WingGroup.Wing.root_chord, 0.,     self.z_offset])
        self.logger.debug(f"{self.pos = }")
        self.weight_self()
