from detailedDesign.classes.Component import Component
import numpy as np
import matplotlib.pyplot as plt


class FuelContainer(Component):
    def __init__(self, Fuselage, design_config):
        super().__init__(design_config)

        self.Fuselage = Fuselage
        self.parent = self.Fuselage

        # self.RemovableContainers = []
        # self.NonRemovableContainers = []
        # self.components = self.RemovableContainers + self.NonRemovableContainers

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self.thickness = None
        self.inner_diameter = None
        self.inner_radius = None

        self.volume_tank = None
        self.length_cyl = None
        self.voltage = None
        self.flow_H2 = None
        self.mass_H2 = None
        self.reserve_mass_H2 = None
        self.volume_tank = None
        self.radius_tank = None
        self.mass_tank = None
        self.area_tank = None
        self.current_fuel_mass = 0

        self.SF = 1.5

        self.thickness_insulation = None
        self.total_tank_thickness = 0.1 
        self.empty_space_thickness = 0.1  # [m] - the space between the fuselage and the tank, must be more than insulation

        self._freeze()

    def weight_self(self):
        state = self.Fuselage.FuselageGroup.Aircraft.states['cruise']

        # normally the radius is found through this eq
        self.mass_tank = self.tank_density * (4 / 3 * np.pi * (self.radius_tank + self.thickness) ** 3 + np.pi * (
                self.radius_tank + self.thickness) ** 2 * self.length_cyl - self.volume_tank) * self.shape_factor

        self.area_tank = 4 * np.pi * self.radius_tank ** 2 + 2 * np.pi * self.radius_tank * self.length_cyl

        # Insulation mass/thickness sizing
        thickness_insulation = np.arange(0.001, 0.01, 0.000001)
        Q_conduction = self.thermal_cond * (self.temp_room - self.temp_LH2) / thickness_insulation
        Q_flow = Q_conduction * self.area_tank
        boiloff_rate = Q_flow / self.E_boiloff
        total_boiloff = boiloff_rate * state.duration
        mass_insulation = self.area_tank * thickness_insulation * self.density_insulation
        mass_total = total_boiloff + self.mass_tank + mass_insulation
        self.own_mass = np.array(mass_total).min()
        self.own_mass = self.own_mass
        index = np.argmin(np.array(mass_total))
        self.thickness_insulation = thickness_insulation[index]
        self.total_tank_thickness = self.thickness_insulation + self.thickness
        self.empty_space_thickness = self.total_tank_thickness

        # # plotting
        # plt.plot(thickness_insulation*1000, mass_total)
        # plt.ylabel("Total mass boiloff, tank, insulation [kg]")
        # plt.xlabel("Insulation thickness [mm]")
        # plt.title("Effect of insulation thickness on total tank weight")
        # plt.grid()
        # plt.xticks(fontsize=11)
        # plt.yticks(fontsize=11)
        # plt.tight_layout()
        # plt.show()

    def size_self(self):
        state = self.Fuselage.FuselageGroup.Aircraft.states["cruise"]

        # Tank thickness sizing
        self.inner_diameter = np.sqrt(
            4 * self.Fuselage.ForwardFuelContainer.outer_area / np.pi) - self.empty_space_thickness * 2 - 2 * self.total_tank_thickness
        # self.inner_diameter = 10 #manual change for non-integral tank
        self.radius_tank = self.inner_diameter / 2  # for integral tank
        self.radius_tank = self.radius_tank  # change here if non-integral tank

        thickness_fatigue = self.tank_pressure * self.radius_tank * self.SF / self.fatiguestrength
        thickness_yield = self.tank_pressure * self.radius_tank * self.SF / self.yieldstrength

        # Should really be: thickness_yield = self.tank_pressure * self.radius_tank * self.SF / (2*self.yieldstrength)
        self.thickness = max(thickness_fatigue, thickness_yield)

        # Debugging
        # self.logger.debug(f"{ self.inner_diameter = }")
        # self.logger.debug(f" { self.radius_tank = }, {self.mass_tank = }")
        # self.logger.debug(f"Empty thickness before: {self.empty_space_thickness} m")
        # self.logger.debug(f"Empty thickness after: {self.empty_space_thickness} m")
        # self.logger.debug(f"Empty space thickness: {self.empty_space_thickness:.4E} [m]")
        # self.logger.debug(f"Insulation thickness: {self.thickness_insulation} [m]")
        self.logger.debug(f"Metal tank thickness: {self.thickness:.4E} [m]")
        self.logger.debug(f"Total tank thickness: {self.total_tank_thickness:.4E} [m]")
        # self.logger.debug(f"Total hydrogen mass: {self.mass_H2:.4E} [kg]")
        # self.logger.debug(f"Total tank mass: {self.own_mass:.4E} [kg]")
        # self.logger.debug(f"Total tank volume: {self.volume_tank:.4E} [m3]")



    def cg_self(self):

        x_cg = 0.5 * self.length_cyl + self.radius_tank + self.total_tank_thickness
        y_cg = 0
        z_cg = 0
        self.own_cg = np.array([x_cg, y_cg, z_cg])

    @property
    def total_length(self):
        return self.length_cyl + 2 * self.radius_tank + self.total_tank_thickness * 2

    def get_mass(self):
        total_mass = self.own_mass + self.current_fuel_mass
        return total_mass

    @property
    def length(self):
        return self.length_cyl + 2 * self.radius_tank + 2 * self.total_tank_thickness

    @property
    def cow_mass(self):
        return self.own_mass + self.current_fuel_mass
