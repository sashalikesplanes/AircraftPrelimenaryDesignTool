# To check
from detailedDesign.classes.Component import Component
from misc.unitConversions import *
import numpy as np


# test


class VerticalTail(Component):
    def __init__(self, Tail, design_config):
        super().__init__(design_config)

        self.Tail = Tail

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self.tail_length = None  # [m]
        self.surface_area = None  # [m2]
        self.mean_geometric_chord = None  # [m]
        self.span = None  # [m]
        self.root_chord = None  # [m]
        self.quarter_chord_sweep = None  # [rad]

        self._freeze()

    def size_self(self):
        self.size_self_geometry()
        self.size_self_mass()
        self.pos = np.array([- self.mean_geometric_chord, 0., 0.])

    def size_self_geometry(self):
        # Sizing dimensions
        wing_area = self.Tail.FuselageGroup.Aircraft.reference_area  # [m2]
        wing_span = self.Tail.FuselageGroup.Aircraft.WingGroup.Wing.span  # [m]
        # Fuselage semi minor and major dimensions (eclipse)
        fuselage_a = self.Tail.FuselageGroup.Fuselage.outer_height / 2
        fuselage_b = self.Tail.FuselageGroup.Fuselage.outer_width / 2

        self.tail_length = np.sqrt(
            (2 * self.volume_coefficient * wing_area * wing_span) / (np.pi * (fuselage_a + fuselage_b)))  # [m]

        self.surface_area = (self.volume_coefficient * \
                             wing_area * wing_span) / self.tail_length  # [m2]

        self.span = np.sqrt(self.aspect_ratio * self.surface_area)  # [m]

        average_chord = self.span / self.aspect_ratio  # [m]
        self.root_chord = (2 * average_chord) / (1 + self.taper)  # [m]
        self.mean_geometric_chord = 2 / 3 * self.root_chord * (
                (1 + self.taper + self.taper ** 2) / (1 + self.taper))  # [m]

    def size_self_mass(self):
        # Sizing mass
        WingGroup = self.Tail.FuselageGroup.Aircraft.WingGroup
        FuselageGroup = self.Tail.FuselageGroup

        state = WingGroup.Aircraft.states["cruise"]

        q = pa_to_psf(0.5 * state.density * state.velocity ** 2)  # [psf]
        n_z = FuselageGroup.Aircraft.ultimate_load_factor  # [-]
        W_O = kg_to_lbs(FuselageGroup.Aircraft.mtom)  # [lbs]
        thickness_to_chord = WingGroup.Wing.thickness_chord_ratio  # [-]
        F_tail = 1  # [0 for conventional, 1 for T-tail]

        self.quarter_chord_sweep = np.arctan(np.tan(self.leading_edge_sweep + self.root_chord / (2 * self.span)
                                                    * (self.taper - 1)))  # [rad]

        mass_lbs = 0.073 * (1 + 0.2 * F_tail) * ((n_z * W_O) ** 0.376) * (q ** 0.122) * (m2_to_ft2(self.surface_area) ** 0.873) * (((100 * thickness_to_chord) / np.cos(self.quarter_chord_sweep)) ** (-0.49)) * ((self.aspect_ratio / (np.cos(self.quarter_chord_sweep) ** 2)) ** 0.357) * (self.taper ** 0.039)

        self.own_mass = lbs_to_kg(mass_lbs)  # [kg]

    def cg_self(self):
        x_cg = 0.4 * self.mean_geometric_chord
        y_cg = 0
        z_cg = -self.span/3
        self.own_cg = np.array([x_cg, y_cg, z_cg])
