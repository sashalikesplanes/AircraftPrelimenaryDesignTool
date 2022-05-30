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
        self.volume_tank = None
        self.radius_tank = None
        self.mass_tank = None
        self.area_tank = None

        self.SF = 1.5

        self.thickness_insulation = None
        self.total_tank_thickness = None

        self._freeze()

    def size_self(self):
        # basic sizing
        # self.empty_space_thickness = 0
        self.inner_diameter = self.Fuselage.inner_diameter - self.empty_space_thickness * 2
        # self.inner_diameter = 10 #manual change for non-integral tank
        self.inner_radius = self.inner_diameter/2  # for integral tank
        self.radius_tank = self.inner_radius  # change here if non-integral tank

        thickness_fatigue = self.tank_pressure * \
            self.inner_radius*self.SF/self.fatiguestrength
        thickness_yield = self.tank_pressure*self.inner_radius*self.SF/self.yieldstrength
        self.thickness = max(thickness_fatigue, thickness_yield)

        # Fuel tank sizing
        # powertest = 132000000  # CHANGE THIS!!!!
        # self.mass_H2 = powertest * self.Fuselage.FuselageGroup.Power.FuelCells.duration_flight / (
        #     32167 * self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency)

        peakpower = self.Fuselage.FuselageGroup.Power.own_power_peak
        averagepower = self.Fuselage.FuselageGroup.Power.own_power_average
        duration_peak = 0.5  # [h] TODO: find the right value (Take off, etc...)
        mass_H2_peak = peakpower * duration_peak / (
            32167 * self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency)
        mass_H2_average = averagepower * (self.Fuselage.FuselageGroup.Power.FuelCells.duration_flight-duration_peak) / (
            32167 * self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency)
        self.mass_H2 = mass_H2_peak+mass_H2_average

        self.volume_tank = self.mass_H2*(1+self.Vi)/self.density_H2
        self.length = (self.volume_tank - 4*np.pi*self.inner_radius**3/3)/(np.pi *
                                                                           self.inner_radius**2)  # we constrained the radius as being an integral tank,\
        # normally the radius is found through this eq
        self.mass_tank = self.tank_density * (4 / 3 * np.pi * (self.radius_tank + self.thickness) ** 3 + np.pi * (
            self.radius_tank + self.thickness) ** 2 * self.length - self.volume_tank)
        self.area_tank = 4 * np.pi * self.radius_tank ** 2 + \
            2 * np.pi * self.radius_tank * self.length

        # calculations mass/thickness
        thickness_insulation = np.arange(0.001, 0.09, 0.000001)
        Q_conduction = self.thermal_cond * (self.temp_room - self.temp_LH2) / thickness_insulation
        Q_flow = Q_conduction * self.area_tank
        boiloff_rate = Q_flow / self.E_boiloff
        total_boiloff = boiloff_rate * \
                        self.Fuselage.FuselageGroup.Power.FuelCells.duration_flight * 3600
        mass_insulation = self.area_tank * thickness_insulation * self.density_insulation
        mass_total = total_boiloff + self.mass_tank + mass_insulation

        self.own_mass = np.array(mass_total).min()
        index = np.argmin(np.array(mass_total))
        self.thickness_insulation = thickness_insulation[index]
        self.total_tank_thickness = self.thickness_insulation + self.thickness

        self.empty_space_thickness = self.total_tank_thickness

        # self.logger.debug(f"Empty space thiccness: {self.empty_space_thickness} [m]")
        self.logger.debug(f"Total tank thiccness: {self.total_tank_thickness} [m]")
        self.logger.debug(f"Total hydrogen mass: {self.mass_H2} [kg]")
        self.logger.debug(f"Total tank mass: {self.own_mass} [kg]")

        # print(f"I am the mass of the fuel contrainer {self.own_mass}")
        # self.Fuselage.FuselageGroup.Aircraft.fuel_mass = self.mass_H2
        # self.own_mass = np.array(mass_total).min()
        # self.Fuselage.FuselageGroup.Aircraft.fuel_mass = self.mass_H2
        # if self.Fuselage.FuselageGroup.Aircraft.debug:

        # plotting
        # plt.plot(thickness_insulation, mass_total)
        # plt.ylabel("Total mass boiloff, tank, insulation [kg]")
        # plt.xlabel("Insulation thickness [m]")
        # plt.title("Effect of insulation thickness on total tank weight")
        # plt.show()


