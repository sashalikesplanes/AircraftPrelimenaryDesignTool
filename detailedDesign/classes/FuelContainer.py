from detailedDesign.classes.Component import Component
import numpy as np


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
        self.inner_diameter = None
        self.inner_radius = None



        # self.fatiguestrength = 103*10**6 #[MPa], fatigue strength Al 2219-T81 after 500e6 cycles
        # self.yieldstrength = 352*10**6 #[MPa], yield strength Al 2219-T81
        self.SF = 1.5

        # self.density_H2 = 71 # [kg/m3], density LH2
        # self.Vi = 0.072 # extra volume needed for boiloff (literature)

        self._freeze()

    def size_self(self):

        self.inner_diameter = self.Fuselage.inner_diameter - self.thickness * 2
        self.inner_radius = self.inner_diameter/2

        self.thickness_fatigue = self.tank_pressure*self.inner_radius*self.SF/self.fatiguestrength
        self.thickness_yield = self.tank_pressure*self.inner_radius*self.SF/(self.yieldstrength)

        self.volume_tank = self.mass_H2*(1+self.Vi)/self.density_H2
        self.length = (self.volume_tank - 4*np.pi*self.inner_radius**3/3)/(np.pi*self.inner_radius**2) # we constrained the radius as being an integral tank,\
                                                                                                                #normally the radius is found through this eq

        self.voltage = 1.2*self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency
        # self.power_produced = self.voltage*Aircraft.FuselageGroup.Power.FuelCells.current_density* areafuelcell


        self.powertest = 600000000

        self.flow_H2 = self.powertest/(self.voltage*self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency*2*96500*500) #GET POWER FROM PAULA
        self.mass_H2 = self.flow_H2*self.Fuselage.FuselageGroup.Power.FuelCells.duration_flight/(32167*self.Fuselage.FuselageGroup.Power.FuelCells.conversion_efficiency)

        self.volume_tank = self.mass_H2* (1+self.Vi)/self.density_H2
        self.radius_tank = self.inner_radius
        self.mass_tank = self.tank_pressure*4/3*np.pi*(self.radius_tank+self.thickness_fatigue)**3+np.pi*(self.radius_tank+self.thickness_fatigue)**2*self.length-self.volume_tank