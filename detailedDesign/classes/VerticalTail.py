# To check
from detailedDesign.classes.Component import Component
from misc.unitConversions import *
import numpy as np


class VerticalTail(Component):
    def __init__(self, Tail, design_config):
        super().__init__(design_config)

        self.Tail = Tail

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self.tail_length = None
        self.surface_area = None
        self.mean_geometric_chord = None
        self.span = None

        self._freeze()

    def size_self(self):
        # Mass Sizing
        WingGroup = self.Tail.FuselageGroup.Aircraft.WingGroup
        FuselageGroup = self.Tail.FuselageGroup

        state = WingGroup.Aircraft.states["cruise"]

        q = pa_to_psi(0.5 * state.density * state.velocity ** 2)    # [psi]
        n_z = FuselageGroup.Aircraft.ultimate_load_factor   # [-]
        W_O = kg_to_lbs(FuselageGroup.Aircraft.mtom)    # [lbs]
        thickness_to_chord = WingGroup.Wing.thickness_chord_ratio   # [-]
        F_tail = 1  # [0 for conventional, 1 for T-tail]

        # TODO: Size these properly
        S_VT = None  # [ft2]
        sweep_VT = None   # [-]
        taper_VT = None   # [-]
        aspect_ratio_VT = None  # [-]

        mass_lbs = 0.073 * (1 + 0.2 * F_tail) * (n_z * W_O) ** 0.376 * q ** 0.122 * S_VT ** 0.873 * (
            (100 * thickness_to_chord) / np.cos(sweep_VT)) ** (-0.49) * (
            aspect_ratio_VT / np.cos(sweep_VT) ** 2) ** 0.357 * taper_VT ** 0.039
        self.own_mass = lbs_to_kg(mass_lbs)  # [kg]
