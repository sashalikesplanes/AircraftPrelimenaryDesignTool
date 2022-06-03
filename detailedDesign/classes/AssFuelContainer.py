from detailedDesign.classes.FuelContainer import FuelContainer
import numpy as np
import matplotlib.pyplot as plt


class AssFuelContainer(FuelContainer):
    def __init__(self, Fuselage, design_config):
        super().__init__(Fuselage, design_config)

    def size_self(self):
        super().size_self()

        self.mass_H2 = self.Fuselage.FuselageGroup.Power.mass_H2 - self.Fuselage.ForwardFuelContainer.mass_H2 - self.Fuselage.AftFuelContainer.mass_H2
        self.volume_tank = self.mass_H2 / self.density_H2 * (1 + self.Vi)

        self.inner_radius = self.Fuselage.inner_ass_diameter / 2

        self.length = (self.volume_tank - 4 / 3 * np.pi * self.inner_radius ** 3) / (np.pi * self.inner_radius ** 2)
        self.logger.debug(f"{self.length = }")
        if self.length < 0:
            self.logger.warn("WARNING ASS FUEL TANK NEGATIVE")
            self.length = 0.1
            self.radius_tank = (self.volume_tank * 3 / 4 / np.pi) ** (1 / 3)

        self.pos = np.array([self.Fuselage.Cabin.length + self.Fuselage.cockpit_length, 0.,     self.z_offset])
        self.logger.debug(f"{self.pos = }")
        self.weight_self()

        if self.own_mass < 5 or np.isnan(self.own_mass):
            self.own_mass = 0.1
