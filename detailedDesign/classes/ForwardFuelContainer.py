from detailedDesign.classes.FuelContainer import FuelContainer
import numpy as np
import matplotlib.pyplot as plt


class ForwardFuelContainer(FuelContainer):
    def __init__(self, Fuselage, design_config):
        super().__init__(Fuselage, design_config)

    def size_self(self):
        super().size_self()

        self.length_cyl = self.Fuselage.FuselageGroup.Aircraft.x_lemac - self.Fuselage.cockpit_length - 2 * self.radius_tank

        # self.volume_tank = 4 / 3 * np.pi * self.radius_tank ** 3 + np.pi * self.radius_tank ** 2 * (self.length - self.radius_tank * 2)
        self.volume_tank = 4 / 3 * np.pi * self.radius_tank ** 3 + np.pi * self.radius_tank ** 2 * (self.length_cyl)

        self.mass_H2 = self.volume_tank * self.density_H2 / (1 + self.Vi)

        self.pos = np.array([self.Fuselage.cockpit_length, 0.,     self.z_offset])

        self.weight_self()
        self.logger.debug(f"{self.length_cyl = }")
        self.logger.debug(f"{self.volume_tank = }")
        self.logger.debug(f"{self.mass_H2 = }")
        self.logger.debug(f"{self.own_mass = }")
