from detailedDesign.classes.FuelContainer import FuelContainer
import numpy as np
import matplotlib.pyplot as plt


class AssFuelContainer(FuelContainer):
    def __init__(self, Fuselage, design_config):
        super().__init__(Fuselage, design_config)

    def size_self(self):
        super().size_self()

        self.mass_H2 = self.Fuselage.FuselageGroup.Power.mass_H2 - self.Fuselage.ForwardFuelContainer.mass_H2 - self.Fuselage.AftFuelContainer.mass_H2
        if self.mass_H2 < 0: 
            self.mass_H2 = 0
        self.logger.debug(f"{self.Fuselage.FuselageGroup.Power.mass_H2 =}")
        self.logger.debug(f"{self.Fuselage.ForwardFuelContainer.mass_H2 = }")
        self.logger.debug(f"{self.Fuselage.AftFuelContainer.mass_H2 = }")
        self.logger.debug(f"{self.mass_H2 = }")
        self.volume_tank = self.mass_H2 / self.density_H2 * (1 + self.Vi)

        self.radius_tank = self.Fuselage.inner_ass_diameter / 2

        self.length_cyl = (self.volume_tank - 4 / 3 * np.pi * self.radius_tank ** 3) / (np.pi * self.radius_tank ** 2)
        self.logger.debug(f"{self.length_cyl = }")
        if self.length_cyl < 0:
            self.logger.warn("WARNING ASS FUEL TANK NEGATIVE")
            self.length_cyl = 0
            self.radius_tank = (self.volume_tank * 3 / 4 / np.pi) ** (1 / 3)

        self.pos = np.array([self.Fuselage.Cabin.length + self.Fuselage.cockpit_length, 0.,     self.z_offset])
        self.logger.debug(f"{self.pos = }")
        self.weight_self()

        self.logger.debug(f"{self.own_mass = }")

        #if self.own_mass < 5 or np.isnan(self.own_mass):
        #    self.own_mass = 0.1
