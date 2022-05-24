# To check
import numpy as np

from detailedDesign.classes.Component import Component
from misc.unitConversions import *


class HorizontalTail(Component):
    def __init__(self, Tail, design_config):
        super().__init__(design_config)

        self.Tail = Tail

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        # Mass Sizing
        WingGroup = self.Tail.FuselageGroup.Aircraft.WingGroup
        FuselageGroup = self.Tail.FuselageGroup

        state = WingGroup.Aircraft.states["cruise"]
        q = pa_to_psi(0.5 * state.density * state.velocity ** 2)
        n_z = FuselageGroup.Aircraft.ultimate_load_factor
        W_O = kg_to_lbs(FuselageGroup.Aircraft.mtom)
        S_HT = None       # [ft2]
        thickness_to_chord = WingGroup.Wing.thickness_chord_ratio
        sweep_HT = None
        taper_HT = None
        l_FS = FuselageGroup.Fuselage.Cabin.length + \
            FuselageGroup.Fuselage.FuelContainer.length
        # TODO: check MDN
        MAGICAL_DISNEY_NUMBER = 0.55
        l_HT = l_FS * MAGICAL_DISNEY_NUMBER     # [ft]
        span_HT = None                  # [ft]
        root_chord_thickness_HT = None   # [inches]
        aspect_ratio_HT = None   # [-]

        self.own_mass = 0.016*(n_z*W_O)**0.414*q**0.168*S_HT**0.896*((100*thickness_to_chord) / np.cos(
            sweep_HT))**(-0.12)*(aspect_ratio_HT/np.cos(sweep_HT)**2)**0.043*taper_HT**(-0.02)

        # state = self.WingGroup.Aircraft.states["cruise"]
        # q = pa_to_psi(0.5 * state.density * state.velocity ** 2)
        # S_W = m2_to_ft2(self.wing_area)
        # W_FW = 1  # Fuel in wings. There is no fuel in the wings therefore = 1
        # sweep = np.pi / 180. * self.sweep  # put it in radians
        # n_z = self.FuselageGroup.Aircraft.ultimate_load_factor
        # W_O = kg_to_lbs(self.FuselageGroup.Aircraft.mtom)
        #
        # self.own_mass = 0.036 * S_W ** 0.758 * W_FW ** 0.0035 * (
        #             self.aspect_ratio / np.cos(sweep) ** 2) ** 0.6 * q ** 0.006 * self.taper_ratio ** 0.04 * (
        #                             (100 * self.thickness_chord_ratio) / np.cos(sweep)) ** (-0.3) * (n_z * W_O) ** 0.49
