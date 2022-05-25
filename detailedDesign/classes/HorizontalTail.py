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
        self.mean_geometric_chord = None
        self.span = None
        self.root_chord = None

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()

    def size_self(self):
        self.size_self_geometry()
        self.size_self_mass()

    def size_self_geometry(self):
        #Sizing dimensions
        wing_area = self.Tail.FuselageGroup.Aircraft.reference_area
        wing_mean_geometric_chord = self.Tail.FuselageGroup.Aircraft.WingGroup.Wing.mean_geometric_chord
        fuselage_radius = self.Tail.FuselageGroup.Fuselage.outer_diameter / 2

        self.tail_length = np.sqrt((2 * self.volume_coefficient * wing_area * wing_mean_geometric_chord \
            )/(np.pi * (2 * fuselage_radius)))

        self.surface_area = (self.volume_coefficient * wing_area * wing_mean_geometric_chord) / self.tail_length   # [ft2]

        self.span = np.sqrt(self.aspect_ratio * self.surface_area)  # [ft]

        average_chord = self.span / self.aspect_ratio
        self.root_chord = (2 * average_chord)/(1 + self.taper)  # [inches]
        self.mean_geometric_chord = 2/3 * self.root_chord * ((1+ self.taper +self.taper**2)/(1+ self.taper))
        

    def size_self_mass(self):
        #Sizing mass
        WingGroup = self.Tail.FuselageGroup.Aircraft.WingGroup
        FuselageGroup = self.Tail.FuselageGroup

        state = WingGroup.Aircraft.states["cruise"]

        q = pa_to_psi(0.5 * state.density * state.velocity ** 2)   # [psi]
        n_z = FuselageGroup.Aircraft.ultimate_load_factor   # [-]
        W_O = kg_to_lbs(FuselageGroup.Aircraft.mtom)   # [lbs]

        thickness_to_chord = WingGroup.Wing.thickness_chord_ratio   # [-]

        l_FS_m = FuselageGroup.Fuselage.length
        l_FS = m_to_ft(l_FS_m)   # [ft]

        # TODO: check MDN

        mass_lbs = 0.016 * (n_z * W_O) ** 0.414 * q ** 0.168 * self.surface_area ** 0.896 * ((100 * thickness_to_chord) / np.cos(
            self.quarter_chord_sweep)) ** (-0.12) * (self.aspect_ratio / np.cos(self.quarter_chord_sweep) ** 2) ** 0.043 * self.taper ** (-0.02)

        self.own_mass = lbs_to_kg(mass_lbs)  # [kg]
