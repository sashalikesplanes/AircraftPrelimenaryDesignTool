from detailedDesign.classes.Component import Component
import numpy as np
import matplotlib.pyplot as plt


class FuelContainer(Component):
    def __init__(self, Fuselage, design_config):
        super().__init__(design_config)

        self.Fuselage = Fuselage

        # self.RemovableContainers = []
        # self.NonRemovableContainers = []
        # self.components = self.RemovableContainers + self.NonRemovableContainers

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self.thickness = None
        self.inner_diameter = None
        self.inner_radius = None

        self.volume_tank = None
        self.length = None
        self.voltage = None
        self.flow_H2 = None
        self.mass_H2 = None
        self.reserve_mass_H2 = None
        self.volume_tank = None
        self.total_volume = None
        self.radius_tank = None
        self.mass_tank = None
        self.area_tank = None

        self.SF = 1.5

        self.thickness_insulation = None
        self.total_tank_thickness = None
        self.length_tank = None
        self.empty_space_thickness = 0.1 # [m] - the space between the fuselage and the tank, must be more than insulation

        self.n_tanks = None

        self._freeze()

    def size_self(self):
        state = self.Fuselage.FuselageGroup.Aircraft.states["cruise"]

        # Tank thickness sizing
        # self.inner_diameter = self.Fuselage.inner_diameter - self.empty_space_thickness * 2
        # # self.inner_diameter = 10 #manual change for non-integral tank
        # self.logger.debug(f"{ self.inner_diameter = }")
        # self.inner_radius = self.inner_diameter / 2  # for integral tank
        #

        self.radius_tank = 2.5/2  # change here if non-integral tank
        self.length_tank = 12.2  # change here if non-integral tank


        thickness_fatigue = self.tank_pressure * \
                            self.radius_tank * self.SF / self.fatiguestrength
        thickness_yield = self.tank_pressure * self.radius_tank * self.SF / self.yieldstrength

        self.thickness = max(thickness_fatigue, thickness_yield)

        # Fuel mass sizing
        peakpower = self.Fuselage.FuselageGroup.Power.own_power_peak
        averagepower = self.Fuselage.FuselageGroup.Power.own_power_average
        duration_peak = 0.5  # [h] TODO: find the right value (Take off, etc...)
        mass_H2_peak = peakpower * duration_peak / (
                32167 * self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency)
        mass_H2_average = averagepower * (state.duration / 3600 - duration_peak) / (
                32167 * self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency)
        self.reserve_mass_H2 = averagepower * self.Fuselage.FuselageGroup.Aircraft.reserve_duration / (32167 * self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency)

        self.mass_H2 = mass_H2_peak + mass_H2_average + self.reserve_mass_H2


        # Tank sizing
        self.volume_tank = 4/3*np.pi*self.radius_tank**3 + np.pi*self.radius_tank**2*(self.length_tank-2*self.radius_tank)
        self.total_volume = self.mass_H2 * (1 + self.Vi) / self.density_H2

        self.n_tanks = self.total_volume / self.volume_tank

        self.length = self.n_tanks/12 *self.length_tank
        # we constrained the radius as being an integral tank,\
        # self.length = (self.volume_tank - 4 * np.pi * self.inner_radius ** 3 / 3) / (np.pi * self.inner_radius ** 2)

        # If the length is negative we will set it to zero and size the tank radius accordingly
        # if self.length < 0:
        #     self.length = 0
        #     self.radius_tank = (self.volume_tank * 3 / 4 / np.pi) ** (1 / 3)

        # normally the radius is found through this eq
        self.mass_tank = self.tank_density * (4 / 3 * np.pi * (self.radius_tank + self.thickness) ** 3 + np.pi * (
                self.radius_tank + self.thickness) ** 2 * (self.length_tank - 2 * self.radius_tank) - self.volume_tank) * self.n_tanks
        self.logger.debug(f" { self.length_tank = }, {self.mass_tank = }")
        
        self.logger.debug(f"{self.volume_tank = }")

        self.area_tank = 4 * np.pi * self.radius_tank ** 2 + 2 * np.pi * self.radius_tank * self.length_tank

        # Insulation mass/thickness sizing
        thickness_insulation = np.arange(0.001, 0.09, 0.000001)
        Q_conduction = self.thermal_cond * (self.temp_room - self.temp_LH2) / thickness_insulation
        Q_flow = Q_conduction * self.area_tank
        boiloff_rate = Q_flow / self.E_boiloff
        total_boiloff = boiloff_rate * state.duration
        mass_insulation = self.area_tank * thickness_insulation * self.density_insulation
        mass_total = total_boiloff + self.mass_tank + mass_insulation
        # self.logger.debug
        self.own_mass = np.array(mass_total).min()
        # self.own_mass = self.own_mass
        index = np.argmin(np.array(mass_total))
        self.thickness_insulation = thickness_insulation[index]
        self.total_tank_thickness = self.thickness_insulation + self.thickness
        self.logger.debug(f"Empty thickness before: {self.empty_space_thickness} m")
        self.empty_space_thickness = self.total_tank_thickness
        self.logger.debug(f"Empty thickness after: {self.empty_space_thickness} m")




        # Debugging
        # self.logger.debug(f"Empty space thiccness: {self.empty_space_thickness:.4E} [m]")
        self.logger.debug(f"Metal tank thiccness: {self.thickness:.4E} [m]")
        self.logger.debug(f"Total tank thiccness: {self.total_tank_thickness:.4E} [m]")
        self.logger.debug(f"Total hydrogen mass: {self.mass_H2:.4E} [kg]")
        self.logger.debug(f"Total tank mass: {self.own_mass:.4E} [kg]")
        self.logger.debug(f"Total tank volume: {self.volume_tank:.4E} [m3]")

        self.logger.debug(f"number of tanks: {self.n_tanks:.4E} [m]")
        # plotting
        # plt.plot(thickness_insulation, mass_total)
        # plt.ylabel("Total mass boiloff, tank, insulation [kg]")
        # plt.xlabel("Insulation thickness [m]")
        # plt.title("Effect of insulation thickness on total tank weight")
        # plt.show()
        self.pos = np.array([self.Fuselage.cockpit_length + self.Fuselage.Cabin.length, 0., 0.])

    def cg_self(self):
        x_cg = 0.5 * self.length + self.inner_radius + self.total_tank_thickness
        y_cg = 0
        z_cg = 0
        self.own_cg = np.array([x_cg, y_cg, z_cg])
