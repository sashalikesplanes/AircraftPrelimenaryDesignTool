import numpy as np

from detailedDesign.classes.Component import Component
from detailedDesign.classes.Cabin import Cabin
from detailedDesign.classes.FuelContainer import FuelContainer
from detailedDesign.classes.CargoBay import CargoBay
from misc.ISA import getPressure
from misc.unitConversions import *


class Fuselage(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)
        self.FuselageGroup = FuselageGroup

        self.CargoBay = CargoBay(self, self.design_config)
        self.Cabin = Cabin(self, self.design_config)
        self.FuelContainer = FuelContainer(self, self.design_config)
        self.components = [self.CargoBay, self.Cabin, self.FuelContainer]
        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        # Dimensions
        self.diameter = None

        self._freeze()

    def size_self(self):
        self.diameter = 1.045 * self.Cabin.diameter + 0.084

        # if self.CargoBay.width is not None:
        #     S_cabin = self.Cabin.width * self.Cabin.height
        #     S_cargo = self.CargoBay.width * self.CargoBay.height

        #     Print dead space inside the fuselage
        #     print(np.pi * self.diameter ** 2 / 4 - S_cargo - S_cabin)

        # MAKE MASS OF THING
        state = self.FuselageGroup.Aircraft.states["cruise"]

        l_FS = self.Cabin.length + self.FuelContainer.length
        S_FUS = np.pi * self.diameter ** 2 / 4 * 2 + np.pi * self.diameter * l_FS
        n_z = self.FuselageGroup.Aircraft.ultimate_load_factor
        W_O = kg_to_lbs(self.FuselageGroup.Aircraft.mtom)
        MAGICAL_DISNEY_NUMBER = 0.55
        l_HT = l_FS * MAGICAL_DISNEY_NUMBER
        d_FS = self.diameter
        q = pa_to_psi(0.5 * state.density * state.velocity ** 2)
        V_p = m3_to_ft3(np.pi * self.Cabin.diameter ** 2 / 4 * self.Cabin.length)
        Delta_P = pa_to_psi(getPressure(self.Cabin.cabin_pressure_altitude) - state.pressure)
        if Delta_P < 0:
            Delta_P = 0

        self.own_mass = lbs_to_kg(0.052 * S_FUS ** 1.086 * (n_z * W_O) ** 0.177 * l_HT ** -0.051 * (l_FS / d_FS) ** \
                        -0.072 * q ** 0.241 + 11.9 * (V_p * Delta_P) ** 0.271)

    def get_sized(self):
        for component in self.components:
            component.get_sized()

        self.size_self()
