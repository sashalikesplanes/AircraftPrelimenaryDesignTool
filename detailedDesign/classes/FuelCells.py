import numpy as np

from detailedDesign.classes.Component import Component


class FuelCells(Component):
    def __init__(self, Power, design_config):
        super().__init__(design_config)

        self.Power = Power
        self.parent = self.Power

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self.voltage = None
        self.power_produced = None
        self.flow_H2 = None
        self.numberplates = None
        self.size = None

        self._freeze()

    def size_self(self):
        # use peak power for this, since the fuel stack has to be able to provide this
        power_peak = self.Power.own_power_peak / self.conversion_efficiency

        self.own_mass = power_peak/self.mass_power_density  # [kg]
        self.size = self.own_mass/self.W_Size  # [m3]
        self.logger.debug(f" {self.size = }")
        # TODO Update
        fuselage = self.Power.FuselageGroup.Fuselage
        self.pos = np.array([fuselage.Cabin.length + fuselage.cockpit_length, 0, 0])


        # self.voltage = 1.2*self.conversion_efficiency*self.amount_cells
        # self.numberplates = power_peak / (self.voltage * self.current_density * self.size)
        # self.power_produced = power_peak/self.numberplates #power that has to be/will be produced per plate
        # self.area_fuelcell = self.power_produced / (self.voltage * self.current_density)

        #
        # # self.power_produced = self.voltage*self.Power.FuelCells.current_density* areafuelcell
        # self.flow_H2 = power_peak/(self.voltage*self.conversion_efficiency*2*96500*500)
        # print("mass:", self.mass)
        # print("total size:", self.size)
        # print("number of plates:",self.numberplates)
        # print("power produced per plate", self.power_produced)

    def cg_self(self):
        self.own_cg = np.array([0, 0., 0.])
