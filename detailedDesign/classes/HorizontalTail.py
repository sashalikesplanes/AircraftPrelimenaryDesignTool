# To check
import numpy as np
from detailedDesign.classes.Component import Component
from misc.unitConversions import *


class HorizontalTail(Component):
    def __init__(self, Tail, design_config):
        super().__init__(design_config)

        self.Tail = Tail

        self.MGC = 1

        self.tail_length = None
        self.surface_area = None
        self.mean_aerodynamic_chord = None
        self.span = None

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        # Mass Sizing
        WingGroup = self.Tail.FuselageGroup.Aircraft.WingGroup
        FuselageGroup = self.Tail.FuselageGroup

        state = WingGroup.Aircraft.states["cruise"]

        q = pa_to_psi(0.5 * state.density * state.velocity ** 2)   # [psi]
        n_z = FuselageGroup.Aircraft.ultimate_load_factor   # [-]
        W_O = kg_to_lbs(FuselageGroup.Aircraft.mtom)   # [lbs]

        S_HT = None  # [ft2]
        thickness_to_chord = WingGroup.Wing.thickness_chord_ratio   # [-]
        sweep_HT = None   # [-]
        taper_HT = None   # [-]
        MGC_HT = None     # [m]

        l_FS_m = FuselageGroup.Fuselage.Cabin.length + \
            FuselageGroup.Fuselage.FuelContainer.length
        l_FS = m_to_ft(l_FS_m)   # [ft]

        # TODO: check MDN
        # TODO: Size these properly

        self.tail_length = np.sqrt((2)/(np.pi * (FuselageGroup.Fuselage.diameter)))
        span_HT = None  # [ft]
        root_chord_thickness_HT = None  # [inches]
        aspect_ratio_HT = None  # [-]

        mass_lbs = 0.016 * (n_z * W_O) ** 0.414 * q ** 0.168 * S_HT ** 0.896 * ((100 * thickness_to_chord) / np.cos(
            sweep_HT)) ** (-0.12) * (aspect_ratio_HT / np.cos(sweep_HT) ** 2) ** 0.043 * taper_HT ** (-0.02)

        self.own_mass = lbs_to_kg(mass_lbs)  # [kg]
