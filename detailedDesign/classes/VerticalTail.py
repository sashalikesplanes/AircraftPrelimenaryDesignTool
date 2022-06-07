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
        self.first_iteration = True  # [-]
        self.F_w = 0

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
        
        #if self.first_iteration:
        #    self.tail_length = np.sqrt(
        #        (2 * self.volume_coefficient * wing_area * wing_span) / (np.pi * (fuselage_a + fuselage_b)))  # [m]
        #    self.first_iteration = False
        #else:
        #    self.tail_length = (self.Tail.FuselageGroup.Fuselage.length - (3/4)*self.mean_geometric_chord) - \
        #    (self.Tail.FuselageGroup.Aircraft.x_lemac + 0.25 * self.Tail.FuselageGroup.Aircraft.WingGroup.Wing.mean_geometric_chord) # [m]

        self.tail_length = self.Tail.HorizontalTail.tail_length

        self.surface_area = (self.volume_coefficient * \
                             wing_area * wing_span) / self.tail_length  # [m2]

        self.span = np.sqrt(self.aspect_ratio * self.surface_area)  # [m]

        average_chord = self.span / self.aspect_ratio  # [m]
        self.root_chord = (2 * average_chord) / (1 + self.taper)  # [m]
        self.mean_geometric_chord = 2 / 3 * self.root_chord * (
                (1 + self.taper + self.taper ** 2) / (1 + self.taper))  # [m]
        # print("initial S",self.surface_area)
        # print(self.surface_area/wing_area)
        # # print("rudder length",self.mean_geometric_chord*0.3)
        # # print("MAC",self.mean_geometric_chord)
        # # print("height VTP",self.span)
        # print("tail length:", self.tail_length)

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

    def size_self_geometry_rudder(self):
        state = self.Tail.FuselageGroup.Aircraft.states["cruise"]

        self.Tail.FuselageGroup.Aircraft.get_cged()
        V_stall = self.Tail.FuselageGroup.Aircraft.clean_stall_speed #TODO: ask for whether this is the correct Vs
        V_appr = 1.1 * V_stall
        V_crosswind = max(0.2*V_stall, 10.288889) #[m/s], 0.2 Vs or 20 kts # = V_w
        V_tot = np.sqrt(V_appr**2+V_crosswind**2)
        self.surface_area=100
        S_s = 1.02*(self.Tail.FuselageGroup.Fuselage.Cabin.length* \
                    self.Tail.FuselageGroup.Fuselage.Cabin.height+self.surface_area)
        d_c = self.Tail.FuselageGroup.Fuselage.Cabin.length - self.Tail.FuselageGroup.Aircraft.get_cg()[0]
        self.F_w = 0.5*state.density*V_crosswind**2*S_s*self.C_d_y
        beta_sideslip = np.arctan(V_crosswind/V_appr)
        C_n_beta = self.Kf2 * self.C_l_alpha_v*(1-self.deta_dbeta)*self.eta_v*self.volume_coefficient
        C_y_beta = -self.Kf1 * self.C_l_alpha_v*(1-self.deta_dbeta)*self.eta_v * \
                   self.surface_area/self.Tail.FuselageGroup.Aircraft.reference_area
        C_n_deltar = -self.C_l_alpha_v*self.volume_coefficient*self.eta_v*self.tau_r*self.br_bv
        C_y_deltar = self.C_l_alpha_v*self.eta_v*self.tau_r*self.br_bv*self.surface_area/self.Tail.FuselageGroup.Aircraft.reference_area

        # self.Tail.FuselageGroup.Aircraft.get_cged()
        # V_stall = 53.65
        # V_appr = 1.1 * V_stall
        # V_crosswind = 20.6  # [m/s], 0.2 Vs or 20 kts # = V_w
        # V_tot = np.sqrt(V_appr ** 2 + V_crosswind ** 2)
        # self.surface_area = 500
        # S_s = 1.02 * (34.3*2.9 + 7)
        # d_c = 34.3/2 - 15.26
        # F_w = 0.5 * state.density * V_crosswind ** 2 * S_s * self.C_d_y
        # beta_sideslip = np.arctan(V_crosswind / V_appr)
        # C_n_beta = self.Kf2 * 4.5 * (1 - 0) * 0.95 * 0.084
        # C_y_beta = -self.Kf1 * 4.5 * (1 - 0) * 0.95 * \
        #            7 / 66
        # C_n_deltar = -4.5 * 0.084 * 0.95 * self.tau_r * 1
        # C_y_deltar = 4.5*0.95*self.tau_r*1*7/66
        #



        # print("Tail area", self.surface_area, "wing area",self.Tail.FuselageGroup.Aircraft.reference_area)
        # print("V_w",V_crosswind, "V_t", V_tot, "Vappr", V_appr)
        # print("Ss",S_s)
        # # print("V_t", V_tot)
        # print("Fw",self.F_w)
        # # print("S",self.Tail.FuselageGroup.Aircraft.reference_area)
        # print("Cnbeta", C_n_beta)
        # print("Cybeta",C_y_beta)
        # print("Cndeltar", C_n_deltar)
        # print("Cydeltar",C_y_deltar)
        # print("beta",beta_sideslip)
        # print("dc", d_c)
        # print("span", self.Tail.FuselageGroup.Aircraft.WingGroup.Wing.span)
        #solve eq 22&23 in https://www.ripublication.com/ijaer18/ijaerv13n10_85.pdf to find the deflections





    def cg_self(self):
        x_cg = 0.4 * self.mean_geometric_chord
        y_cg = 0
        z_cg = -self.span/3
        self.own_cg = np.array([x_cg, y_cg, z_cg])
