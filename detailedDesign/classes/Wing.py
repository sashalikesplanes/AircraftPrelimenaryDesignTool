# To Check
import numpy as np
from detailedDesign.classes.Component import Component
from misc.unitConversions import *
from sympy.solvers import solve
from sympy import Symbol


class Wing(Component):
    def __init__(self, WingGroup, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup
        # self.HLDs = HLDs(self, self.design_config)
        # self.components = [self.HLDs]

        self.wing_area = 0  # Initial Value
        self.span = 0  # Initial Value
        self.tip_chord = 0  # Initial Value
        self.mean_geometric_chord = 0  # Initial Value
        self.root_chord = 0  # Initial Value
        self.sweep = 0  # Initial Value
        self.C_L_alpha = 0  # Initial Value
        self.alpha_zero_lift = -3.0  # [deg]
        self.C_L_0_wing = 0
        self.oswald = 0

        # Create all the parameters that this component must have here:
        # Using self.property_name = None
        self._freeze()
         
    def size_AR(self):
        #this should be used to check the validity of the aspect ratio assumed in the config and shgould be run outside of the iterations
        #at the end when there is a final product to get a guideline on the aspect ratio value
        range = self.WingGroup.Aircraft.states['cruise'].range   # [m]
        range_ft = m_to_ft(range)  # [ft]
        V_C = self.WingGroup.Aircraft.states['cruise'].velocity   # [m/s]
        dynamic_pressure = 0.5 * self.WingGroup.Aircraft.states['cruise'].density \
            * V_C * V_C   # [Pa]
        W_initial_cruise = self.WingGroup.Aircraft.mtom * 9.81   # [N]
        W_end_cruise = self.WingGroup.Aircraft.mtom * 9.81 - 0.8 * self.WingGroup.Aircraft.FuselageGroup.Fuselage.FuelContainer.mass_H2 * 9.81   # [N]
        C_L_initial_cruise = W_initial_cruise / \
            (dynamic_pressure * self.wing_area)    # [-]
        C_L_end_cruise = W_end_cruise / (dynamic_pressure * self.wing_area)    # [-]
        C_LC = (C_L_initial_cruise + C_L_end_cruise) / 2    # [-]

        C_D_min = self.WingGroup.Aircraft.C_D_min    # [-]
        c_t_SI = ((self.WingGroup.Aircraft.FuselageGroup.Fuselage.FuelContainer.mass_H2 * 1000 )/ range) * V_C * (1000/self.WingGroup.Aircraft.reference_thrust)  # [g/kNs]
        c_t_Imp = c_t_SI * 9.81 / 1e6   # [1/s]

        value = (range_ft * c_t_Imp * C_D_min)/(C_LC * np.log(W_initial_cruise/W_end_cruise))

        if m_to_ft(V_C) > value:
            optimal_ARe = ((C_LC * C_LC) / np.pi) * (1 / (((m_to_ft(V_C) / range_ft)
                                                           * (C_LC / c_t_Imp) * np.log(W_initial_cruise
                                                                                       / W_end_cruise)) - C_D_min))
            x = Symbol('x')
            ARs = solve( (0.0801* x )**1.68 - 1.14 * x + optimal_ARe, x , dict = True)
            print(f'The ideal aspect ratios for the range of {range} m are {ARs}.')
            return optimal_ARe, ARs

        else:
            print(f'Not possible to find the ideal aspect ratio for the required range')
            return 'not available', 'not available'


    def determine_C_L_alpha(self):
        V_C = self.WingGroup.Aircraft.states['cruise'].velocity
        speed_of_sound = self.WingGroup.Aircraft.states['cruise'].speed_of_sound
        aspect_ratio = self.aspect_ratio
        beta = np.sqrt((1 - (V_C / speed_of_sound) ** 2))
        k = 0.95  # from Sam
        #this takes into account no sweep for the wing
        semi_chord_sweep = np.arctan(np.tan(self.sweep - (4 / aspect_ratio) * ((0.5-0.25)* ((1 - self.taper_ratio)/(1 + self.taper_ratio)))))  # [rad]
        self.C_L_alpha = (2 * np.pi * aspect_ratio) / (2 + np.sqrt(((aspect_ratio * beta) / k) ** 2
                                                            * (1 + (np.tan(semi_chord_sweep) ** 2) / (beta ** 2)) + 4))

        # print(f'{np.deg2rad(C_L_alpha) = }')
        return np.deg2rad(self.C_L_alpha)

    def get_C_L(self, alpha):
        # ALPHA IS IN DEGREES
        return self.C_L_0_wing + alpha * self.C_L_alpha

    def get_oswald(self):
        return 1.78 * (1 - 0.045 * self.aspect_ratio ** 0.68) - 0.64

    def size_self(self): #parameters unit tested manually: equations are correct
        self.wing_area = self.WingGroup.Aircraft.reference_area

        #self.size_AR()
        self.span = (self.wing_area * self.aspect_ratio) ** 0.5
        self.logger.debug(f"Span: {self.span}")
        self.root_chord = (2 * self.wing_area) / \
                          (self.span * (1 + self.taper_ratio))  # [m]
        self.tip_chord = self.root_chord * self.taper_ratio     # [m]
        self.mean_geometric_chord = (2 / 3) * self.root_chord * \
            ((1 + self.taper_ratio + self.taper_ratio ** 2) / \
             (1 + self.taper_ratio))  # [m]
        self.sweep = 0  # M < 0.7
        self.C_L_alpha = self.determine_C_L_alpha()
        self.C_L_0_wing = -self.alpha_zero_lift * self.C_L_alpha
        self.oswald = self.get_oswald()

        self.logger.debug(f"Root Chord: {self.root_chord}")
        self.logger.debug(f"Tip Chord: {self.tip_chord}")

        # Mass Sizing
        state = self.WingGroup.Aircraft.states["cruise"]

        q = pa_to_psi(0.5 * state.density * state.velocity ** 2)  # [psi]
        S_W = m2_to_ft2(self.wing_area)  # [ft2]
        W_FW = 1  # Fuel in wings. There is no fuel in the wings therefore = 1
        sweep = np.deg2rad(self.sweep)  # [rads]
        n_z = self.WingGroup.Aircraft.ultimate_load_factor
        W_O = kg_to_lbs(self.WingGroup.Aircraft.mtom)  # [lbs]

        mass_lbs = 0.036 * S_W ** 0.758 * W_FW ** 0.0035 \
            * (self.aspect_ratio / np.cos(sweep) ** 2) ** 0.6 * q ** 0.006 \
            * self.taper_ratio ** 0.04 * ((100 * self.thickness_chord_ratio)
                                          / np.cos(sweep)) ** (-0.3) * (n_z * W_O) ** 0.49

        self.own_mass = lbs_to_kg(mass_lbs)  # [kg]
        self.pos = np.array([self.WingGroup.Aircraft.x_lemac, 0., -self.WingGroup.Aircraft.FuselageGroup.Fuselage.outer_diameter/2])

    def cg_self(self):
        x_cg = 0.4 * self.mean_geometric_chord
        y_cg = 0
        z_cg = 0  # might change with changing alpha incidence
        self.own_cg = np.array([x_cg, y_cg, z_cg])