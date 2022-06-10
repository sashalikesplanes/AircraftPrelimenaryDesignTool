from detailedDesign.classes.FuelContainer import FuelContainer
import numpy as np
import matplotlib.pyplot as plt


class AftFuelContainer(FuelContainer):
    def __init__(self, Fuselage, design_config):
        super().__init__(Fuselage, design_config)

    def size_self(self):
        super().size_self()

        self.length_cyl = self.Fuselage.cockpit_length + self.Fuselage.Cabin.length - (self.Fuselage.FuselageGroup.Aircraft.x_lemac + self.Fuselage.FuselageGroup.Aircraft.WingGroup.Wing.root_chord) - 2 * self.radius_tank

        # self.volume_tank = 4 / 3 * np.pi * self.radius_tank ** 3 + np.pi * self.radius_tank ** 2 * (self.length_cyl - 2 * self.radius_tank)
        self.volume_tank = 4 / 3 * np.pi * self.radius_tank ** 3 + np.pi * self.radius_tank ** 2 * self.length_cyl

        self.mass_H2 = self.volume_tank * self.density_H2 / (1 + self.Vi)

        self.pos = np.array([self.Fuselage.FuselageGroup.Aircraft.x_lemac + self.Fuselage.FuselageGroup.Aircraft.WingGroup.Wing.root_chord, 0.,     self.z_offset])

        self.weight_self()

        if self.length_cyl < 0:
            self.length_cyl = 0
            self.volume_tank = 0
            self.mass_H2 = 0
            self.own_mass = 0

        # self.logger.debug(f"{self.length_cyl = }")
        # self.logger.debug(f"{self.volume_tank = }")
        # self.logger.debug(f"{self.mass_H2 = }")
        # self.logger.debug(f"{self.own_mass = }")
