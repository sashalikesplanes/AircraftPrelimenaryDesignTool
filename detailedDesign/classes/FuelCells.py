# To check
from detailedDesign.classes.Component import Component


class FuelCells(Component):
    def __init__(self, Power, design_config):
        super().__init__(design_config)

        self.Power = Power

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self.voltage = 0
        self.power_produced = 0
        self.flow_H2 = 0
        self.numberplates = 0
        self.mass = 0
        self.size = 0

        self._freeze()

    def size_self(self):
        powertest = 132e6 #[W], CHANGE!!!!

        self.mass = powertest/self.mass_power_density #[kg]
        self.size = self.mass/self.W_Size  #[m3]




        #
        # self.voltage = 1.2*self.conversion_efficiency
        # self.numberplates = powertest / (self.voltage * self.current_density * self.size)
        # self.power_produced = powertest/self.numberplates #power that has to be/will be produced per plate
        # self.area_fuelcell = self.power_produced / (self.voltage * self.current_density)

        #
        # # self.power_produced = self.voltage*self.Power.FuelCells.current_density* areafuelcell
        # self.flow_H2 = powertest/(self.voltage*self.conversion_efficiency*2*96500*500)
        print("mass:", self.mass)
        print("total size:", self.size)
        # print("number of plates:",self.numberplates)
        # print("power produced per plate", self.power_produced)


