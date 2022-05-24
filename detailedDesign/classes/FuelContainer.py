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
        self.thickness = 0
        self.inner_diameter = 0
        self.inner_radius = 0

        self.volume_tank = 0
        self.length = 0
        self.voltage = 0
        self.flow_H2 = 0
        self.mass_H2 = 0
        self.volume_tank = 0
        self.radius_tank = 0
        self.mass_tank = 0
        self.area_tank = 0

        self.SF = 1.5

        self._freeze()

    def size_self(self):
        # basic sizing
        # self.inner_diameter = self.Fuselage.inner_diameter - self.thickness * 2
        self.inner_diameter = 10 #manual change for non-integral tank
        self.inner_radius = self.inner_diameter/2 #for integral tank
        self.radius_tank = self.inner_radius #change here if non-integral tank

        thickness_fatigue = self.tank_pressure*self.inner_radius*self.SF/self.fatiguestrength
        thickness_yield = self.tank_pressure*self.inner_radius*self.SF/self.yieldstrength
        self.thickness = max(thickness_fatigue, thickness_yield)

        #Fuel tank sizing
        powertest = 300000000 #CHANGE THIS!!!!

        self.mass_H2 = powertest * self.Fuselage.FuselageGroup.Power.FuelCells.duration_flight / (
                    32167 * self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency)

        self.volume_tank = self.mass_H2*(1+self.Vi)/self.density_H2
        self.length = (self.volume_tank - 4*np.pi*self.inner_radius**3/3)/(np.pi*self.inner_radius**2) # we constrained the radius as being an integral tank,\
                                                                                                                #normally the radius is found through this eq
        self.mass_tank = self.tank_density * (4 / 3 * np.pi * (self.radius_tank + self.thickness) ** 3 + np.pi * (
                    self.radius_tank + self.thickness) ** 2 * self.length - self.volume_tank)
        self.area_tank = 4 * np.pi * self.radius_tank ** 2 + 2 * np.pi * self.radius_tank * self.length


        #reuse this for fuel cells
        # self.voltage = 1.2*self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency
        # self.power_produced = self.voltage*Aircraft.FuselageGroup.Power.FuelCells.current_density* areafuelcell
        # self.flow_H2 = powertest/(self.voltage*self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency*2*96500*500) #GET POWER FROM PAULA


        #calculations mass/thickness
        thickness_insulation = np.arange(0.001,0.09,0.000001)
        mass_total = []
        for i in thickness_insulation:
            Q_conduction = self.thermal_cond*(self.temp_room-self.temp_LH2)/i
            Q_flow = Q_conduction*self.area_tank
            boiloff_rate = Q_flow/self.E_boiloff
            total_boiloff = boiloff_rate*self.Fuselage.FuselageGroup.Power.FuelCells.duration_flight*3600
            mass_insulation = self.area_tank*i*self.density_insulation
            mass_total.append(total_boiloff+self.mass_tank+mass_insulation)


        #plotting
        # plt.plot(thickness_insulation, mass_total)
        # plt.ylabel("Total mass boiloff, tank, insulation [kg]")
        # plt.xlabel("Insulation thickness [m]")
        # plt.title("Effect of insulation thickness on total tank weight")
        # plt.show()

        #tryout print statements
        # print("mass H2=",self.mass_H2)
        # print("volume tank=",self.volume_tank)
        # print("length=",self.length)
        # print("total boiloff=",total_boiloff)
        # print("mass tank=", self.mass_tank)
        # print("area tank=", self.area_tank)
        # print("thickness tank=", self.thickness)




