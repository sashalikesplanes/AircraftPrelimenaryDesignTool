import numpy as np

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

        self._freeze()

    @property
    def length(self):
        # TODO add nose cone etc
        length = self.Cabin.length
        self.logger.debug(f"Volume of Fuel: {self.ForwardFuelContainer.volume_tank + self.AftFuelContainer.volume_tank + self.AssFuelContainer.volume_tank} m3")
        self.logger.debug(f"Cabin length: {self.Cabin.length}")
        self.logger.debug(f"Fuel Compartment Length: {self.ForwardFuelContainer.length + self.ForwardFuelContainer.radius_tank * 4 + self.AftFuelContainer.length}")
        self.logger.debug(f"Wing box length: {self.FuselageGroup.Aircraft.WingGroup.Wing.root_chord }")

        self.tail_length = 1.6 * self.outer_height   # from ADSEE typical for airliners
        return length + self.cockpit_length + self.AssFuelContainer.length + self.tail_length

    @property
    def thickness(self):
        return (self.inner_height * 1.045 + 0.084 - self.inner_height) / 2

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

        self.bending_shear()

    def cg_self(self):
        self.own_cg = np.array([0.5 * self.length, 0., 0.])

    def get_sized(self):
        for component in self.components:
            component.get_sized()

        self.size_self()

    def bending_shear(self):
        # if (self.FuselageGroup.Fuselage.outer_height == self.FuselageGroup.Fuselage.outer_width):
        #     I_zz = np.pi/64*(self.FuselageGroup.Fuselage.outer_width**4-self.FuselageGroup.Fuselage.inner_width**4)
        #     I_yy = I_zz
        # else:

        # Initialisation
        # z = np.linspace(0, z_max, 100)
        # y = np.linspace(0, y_max, 100)
        t = np.linspace(0, 0.5, 100)
        # t = max(self.FuselageGroup.Fuselage.outer_height/2 - self.FuselageGroup.Fuselage.inner_height/2, self.FuselageGroup.Fuselage.outer_width/2 - self.FuselageGroup.Fuselage.inner_width/2)

        z_max = self.FuselageGroup.Fuselage.outer_height / 2
        z_inner = self.FuselageGroup.Fuselage.inner_height / 2
        y_max = self.FuselageGroup.Fuselage.outer_width / 2
        y_inner = self.FuselageGroup.Fuselage.inner_width / 2
        R = max(z_max, y_max)  # not really sure since it's a cylinder, maybe just take it as a contingency
        # R_inner = max(self.FuselageGroup.Fuselage.inner_width / 2, self.FuselageGroup.Fuselage.inner_height / 2)

        # inertia thin walled oval
        area = 0.25 * np.pi * (
                    self.FuselageGroup.Fuselage.outer_height * self.FuselageGroup.Fuselage.outer_width - self.FuselageGroup.Fuselage.inner_height * self.FuselageGroup.Fuselage.inner_width)
        I_zz = (np.pi * (
                    self.FuselageGroup.Fuselage.outer_height * self.FuselageGroup.Fuselage.outer_width ** 3 - self.FuselageGroup.Fuselage.inner_height * self.FuselageGroup.Fuselage.inner_width ** 3)) / 64
        I_yy = (np.pi * (
                    self.FuselageGroup.Fuselage.outer_height ** 3 * self.FuselageGroup.Fuselage.outer_width - self.FuselageGroup.Fuselage.inner_height ** 3 * self.FuselageGroup.Fuselage.inner_width)) / 64
        J_0 = I_zz + I_yy

        # first moment of area <-hopefully correct
        Q_outer_z = 0.25 * np.pi * z_max * y_max ** 3
        Q_outer_y = 0.25 * np.pi * z_max ** 3 * y_max
        Q_inner_z = 0.25 * np.pi * z_inner * y_inner ** 3
        Q_inner_y = 0.25 * np.pi * z_inner ** 3 * y_inner
        Q_z = Q_outer_z - Q_inner_z
        Q_y = Q_outer_y - Q_inner_y

        delta_P = np.abs(getPressure(self.FuselageGroup.Aircraft.states['cruise'].altitude) - getPressure(0))

        M_z = 0
        M_y = 0
        # loading in y-/z-axis
        S_y = 0
        S_z = 0
        T = 0

        # Stress calculations
        sigma_xA = []
        sigma_xB =[]
        sigma_y = []
        tau = []
        tau_maxA = []
        sigma_1A = []
        sigma_2A = []
        tau_maxB = []
        sigma_1B = []
        sigma_2B = []

        for i in range(len(t)):
            sigma_xA.append(M_z * 0 / I_zz + M_y * z_max / I_yy + 2 * delta_P * R / (2 * t[i]))
            sigma_xB.append(M_z * y_max / I_zz + M_y * 0 / I_yy + 2 * delta_P * R / (2 * t[i]))
            sigma_y.append(2 * delta_P * R / t[i])

            # sigma_x = M_z*y/I_zz + M_y*z/I_yy + 2*delta_P*R/(2*t)
            # sigma_y = 2*delta_P*R/t

            tau.append(-(S_y * Q_z) / (I_zz * t[i]) - (S_z * Q_y) / (I_yy * t[i]) + T * R / J_0)

            tau_maxA.append(np.sqrt(((sigma_xA[i] - sigma_y[i]) / 2) ** 2 + tau[i] ** 2))
            sigma_1A.append((sigma_xA[i] + sigma_y[i]) / 2 + tau_maxA[i])
            sigma_2A.append((sigma_xA[i] + sigma_y[i]) / 2 - tau_maxA[i])

            tau_maxB.append(np.sqrt(((sigma_xB[i] - sigma_y[i]) / 2) ** 2 + tau[i] ** 2))
            sigma_1B.append((sigma_xB[i] + sigma_y[i]) / 2 + tau_maxB[i])
            sigma_2B.append((sigma_xB[i] + sigma_y[i]) / 2 - tau_maxB[i])

        print(sigma_y)
