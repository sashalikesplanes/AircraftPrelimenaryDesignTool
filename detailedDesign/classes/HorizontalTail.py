# To check
import numpy as np
from detailedDesign.classes.Component import Component
from misc.unitConversions import *


class HorizontalTail(Component):
    def __init__(self, Tail, design_config):
        super().__init__(design_config)

        self.Tail = Tail

        self.tail_length = None  # [m]
        self.surface_area = None  # [m2]
        self.mean_geometric_chord = None  # [m]
        self.span = None  # [m]
        self.root_chord = None  # [m]
        self.quarter_chord_sweep = None  # [rad]

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        self.size_self_geometry()
        self.size_self_mass()
        self.pos = np.array([- self.mean_geometric_chord, 0., 0.])

    def size_self_geometry(self):
        # Sizing dimensions
        wing_area = self.Tail.FuselageGroup.Aircraft.reference_area  # [m2]
        # [m]
        wing_mean_geometric_chord = self.Tail.FuselageGroup.Aircraft.WingGroup.Wing.mean_geometric_chord

        fuselage_a = self.Tail.FuselageGroup.Fuselage.outer_height / 2
        fuselage_b = self.Tail.FuselageGroup.Fuselage.outer_width / 2

        self.tail_length = np.sqrt((2 * self.volume_coefficient * wing_area * wing_mean_geometric_chord)/(np.pi * (fuselage_a + fuselage_b)))  # [m]

        self.surface_area = (self.volume_coefficient * wing_area *
                             wing_mean_geometric_chord) / self.tail_length   # [m2]

        self.span = np.sqrt(self.aspect_ratio * self.surface_area)  # [m]

        average_chord = self.span / self.aspect_ratio  # [m]
        self.root_chord = (2 * average_chord)/(1 + self.taper)  # [m]
        self.mean_geometric_chord = 2/3 * self.root_chord * \
            ((1 + self.taper + self.taper**2)/(1 + self.taper))  # [m]

    def size_self_mass(self):
        # Sizing mass
        WingGroup = self.Tail.FuselageGroup.Aircraft.WingGroup
        FuselageGroup = self.Tail.FuselageGroup

        state = FuselageGroup.Aircraft.states["cruise"]

        q = pa_to_psf(0.5 * state.density * state.velocity ** 2)   # [psi]
        n_z = FuselageGroup.Aircraft.ultimate_load_factor   # [-]
        W_O = kg_to_lbs(FuselageGroup.Aircraft.mtom)   # [lbs]

        S_HT = m2_to_ft2(self.surface_area)  # [ft2]
        thickness_to_chord = WingGroup.Wing.thickness_chord_ratio   # [-]

        # TODO: check MDN
        self.quarter_chord_sweep = np.arctan(np.tan(self.three_quarter_chord_sweep) - 4/self.aspect_ratio * ((0.25 - 0.75)*((1 - self.taper)
                                                                                                                            / (1 + self.taper))))  # [rad]

        # this is now literally taken from Raymer, might have to take both sweeps of the horizontal tail
        mass_lbs = 0.016 * ( (n_z * W_O) ** 0.414) * (q ** 0.168 )* (S_HT ** 0.896 )* (((100 * thickness_to_chord) / np.cos(
            WingGroup.Wing.sweep)) ** (-0.12)) * ((self.aspect_ratio / (np.cos(self.quarter_chord_sweep) ** 2)) ** 0.043) * (self.taper ** (-0.02))

        self.own_mass = lbs_to_kg(mass_lbs)  # [kg]

    def cg_self(self):
        x_cg = 0.4 * self.mean_geometric_chord
        y_cg = 0
        z_cg = 0  # Might change with changing alpha incidence
        self.own_cg = np.array([x_cg, y_cg, z_cg])
