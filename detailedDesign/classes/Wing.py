# To Check
import numpy as np
from detailedDesign.classes.Component import Component
from detailedDesign.classes.HLDs import HLDs
from misc.unitConversions import *


class Wing(Component):
    def __init__(self, WingGroup, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup
        self.HLDs = HLDs(self, self.design_config)
        self.components = [self.HLDs]

        self.taper = None

        self.wing_area = None
        self.span = None
        self.tip_chord = None
        self.mean_geometric_chord = None
        self.root_chord = None
        self.sweep = None


        

        # Create all the parameters that this component must have here:
        # Using self.property_name = None
        self._freeze()

    def size_AR(self):
        print(f'sizing the Aspect Ratio')
        range_ = self.WingGroup.Aircraft.states['cruise'].range
        V_C = self.WingGroup.Aircraft.states['cruise'].velocity 
        dynamic_pressure = 0.5 * self.WingGroup.Aircraft.states['cruise'].density * V_C * V_C
        W_initial_cruise = self.WingGroup.Aircraft.mtom * 9.81 
        W_end_cruise = self.WingGroup.Aircraft.mtom * 9.81 * .7
        C_L_initial_cruise = W_initial_cruise / (dynamic_pressure * self.wing_area)
        C_L_end_cruise = W_end_cruise / (dynamic_pressure * self.wing_area)
        C_LC = (C_L_initial_cruise + C_L_end_cruise) / 2

        C_D_min = self.WingGroup.Aircraft.C_D_min
        c_t_SI = self.WingGroup.Engines.thrust_specific_fuel_consumption  # [g/kNs]
        c_t_Imp = c_t_SI * 9.81 / 1e6 * 3600

        optimal_effective_AR = C_LC * C_LC / np.pi / (V_C / range \
                                * C_LC / c_t_Imp * np.log(W_intial_cruise \                                              / W_final_cruise) - C_D_min)
        print(optimal_effective_AR)

    def size_self(self):
        self.wing_area = self.WingGroup.Aircraft.reference_area

        self.size_AR()
        self.span = (self.wing_area * self.aspect_ratio) ** 0.5
        # print(self.span)
        self.root_chord = (2 * self.wing_area) / (self.span * (1 + self.taper_ratio))
        self.tip_chord = self.root_chord * self.taper_ratio

        self.sweep = 0  # M < 0.7
        # print(self.root_chord, self.tip_chord)

        # Mass Sizing
        state = self.WingGroup.Aircraft.states["cruise"]
        q = pa_to_psi(0.5 * state.density * state.velocity ** 2)
        S_W = m2_to_ft2(self.wing_area)
        W_FW = 1  # Fuel in wings. There is no fuel in the wings therefore = 1
        sweep = np.pi / 180. * self.sweep  # put it in radians
        n_z = self.FuselageGroup.Aircraft.ultimate_load_factor
        W_O = kg_to_lbs(self.FuselageGroup.Aircraft.mtom)

        self.own_mass = 0.036 * S_W ** 0.758 * W_FW ** 0.0035  \ 
                    * (self.aspect_ratio / np.cos(sweep) ** 2) ** 0.6 * q ** 0.006 \
                    * self.taper_ratio ** 0.04 * ((100 * self.thickness_chord_ratio) \
                    / np.cos(sweep)) ** (-0.3) * (n_z * W_O) ** 0.49
