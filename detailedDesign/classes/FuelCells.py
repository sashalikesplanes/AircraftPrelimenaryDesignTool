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

        self._freeze()

    def size_self(self):
        pass
        #look in teams, there is an excel for the calculation of mass&size of fuelcells. Ask Kato for questions



        # powertest = 300000000 #CHANGE THIS!!! #this is equal to the full required/output power
        # # areafuelcell = 100 #CHANGE THIS!!!
        #
        # self.voltage = 1.2*self.conversion_efficiency
        # self.power_produced = powertest/self.numberplates #power that has to be/will be produced per plate
        # self.area_fuelcell = self.power_produced / (self.voltage * self.current_density)
        # self.numberplates = powertest / (self.voltage * self.current_density * self.area_fuelcell)
        #
        # # self.power_produced = self.voltage*self.Power.FuelCells.current_density* areafuelcell
        # self.flow_H2 = powertest/(self.voltage*self.conversion_efficiency*2*96500*500)



