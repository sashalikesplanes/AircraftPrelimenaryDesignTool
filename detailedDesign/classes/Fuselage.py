import numpy as np
import matplotlib.pyplot as plt

from detailedDesign.classes.Component import Component
from detailedDesign.classes.Cabin import Cabin
from detailedDesign.classes.ForwardFuelContainer import ForwardFuelContainer
from detailedDesign.classes.AftFuelContainer import AftFuelContainer
from detailedDesign.classes.AssFuelContainer import AssFuelContainer
from detailedDesign.classes.CargoBay import CargoBay
from misc.ISA import getPressure
from misc.unitConversions import *
# from detailedDesign.classes.RemovableFuelContainer import FuelContainer


class Fuselage(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)
        self.FuselageGroup = FuselageGroup
        self.parent = self.FuselageGroup

        self.Cabin = Cabin(self, self.design_config)
        self.Cabin.get_sized()
        self.CargoBay = CargoBay(self, self.design_config)
        self.ForwardFuelContainer = ForwardFuelContainer(self, self.design_config)
        self.AftFuelContainer = AftFuelContainer(self, self.design_config)
        self.AssFuelContainer = AssFuelContainer(self, self.design_config)
        self.components = [self.Cabin, self.CargoBay, self.ForwardFuelContainer, self.AftFuelContainer, self.AssFuelContainer]
        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self.tail_length = 0
        self.fuselage_length = 0
        self.longitudinal_shear = None
        self.longitudinal_moment = None

        self._freeze()

    @property
    def length(self):
        # TODO add nose cone etc
        length = self.Cabin.length
        self.logger.debug(f"Volume of Fuel: {self.ForwardFuelContainer.volume_tank + self.AftFuelContainer.volume_tank + self.AssFuelContainer.volume_tank} m3")
        self.logger.debug(f"Cabin length: {self.Cabin.length}")
        self.logger.debug(f"Fuel Compartment Length: {self.ForwardFuelContainer.length + self.AftFuelContainer.length}")
        self.logger.debug(f"Wing box length: {self.FuselageGroup.Aircraft.WingGroup.Wing.root_chord }")

        self.tail_length = 1.6 * self.outer_height   # from ADSEE typical for airliners

        return length + self.cockpit_length + self.AssFuelContainer.length + self.tail_length

    @property
    def thickness(self):
        return (self.inner_height * 1.045 + 0.084 - self.inner_height) / 2

    @property
    def fuel_tank_mass(self):
        return self.ForwardFuelContainer.get_mass() + self.AssFuelContainer.get_mass() + self.AftFuelContainer.get_mass()

    @property
    def outer_height(self):
        return self.inner_height + self.thickness * 2

    @property
    def outer_width(self):
        return self.inner_width + self.thickness * 2

    def size_self(self):

        # if self.CargoBay.width is not None:
        #     S_cabin = self.Cabin.width * self.Cabin.height
        #     S_cargo = self.CargoBay.width * self.CargoBay.height

        #     Print dead space inside the fuselage
        #     print(np.pi * self.diameter ** 2 / 4 - S_cargo - S_cabin)

        # MAKE MASS OF THING
        a = self.outer_height / 2 # Semi major axis of elipse for easy calcs
        b = self.outer_width / 2 # Semi minor...

        state = self.FuselageGroup.Aircraft.states["cruise"]

        l_FS = m_to_ft(self.length)  # [ft]

        S_FUS_m = (np.pi * a * b) * 2 + \
            np.pi * (a + b) * self.length  # [m2]
        S_FUS = m2_to_ft2(S_FUS_m)  # [ft2]

        n_z = self.FuselageGroup.Aircraft.ultimate_load_factor

        W_O = kg_to_lbs(self.FuselageGroup.Aircraft.mtom)   # [lbs]

        # TODO: check MDN
        MAGICAL_DISNEY_NUMBER = 0.55
        l_HT = l_FS * MAGICAL_DISNEY_NUMBER     # [ft]

        d_FS = m_to_ft((self.outer_height + self.outer_width ) / 2)      # [ft]

        q = pa_to_psf(0.5 * state.density * state.velocity ** 2)  # [psf]

        # TODO Possibly reduce this later
        a_inner = self.inner_height / 2
        b_inner = self.inner_width / 2
        V_p = m3_to_ft3(np.pi * a_inner * b_inner * self.Cabin.length)   # [ft3]

        Delta_P = pa_to_psi(getPressure(
            self.Cabin.cabin_pressure_altitude) - state.pressure)   # [psi]
        if Delta_P < 0:
            Delta_P = 0

        mass_lbs = 0.052 * S_FUS ** 1.086 * (n_z * W_O) ** 0.177 * l_HT ** -0.051 * (
            l_FS / d_FS) ** (-0.072) * q ** 0.241 + 11.9 * (V_p * Delta_P) ** 0.271

        self.own_mass = lbs_to_kg(mass_lbs)

        # self.bending_shear()

    def cg_self(self):
        self.own_cg = np.array([0.5 * self.length, 0., 0.])

    def get_sized(self):
        for component in self.components:
            component.get_sized()

        self.size_self()
