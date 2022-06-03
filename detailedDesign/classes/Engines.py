# To Check
from detailedDesign.classes.Component import Component
import numpy as np
import misc.ISA as ISA

class Engines(Component):
    def __init__(self, WingGroup, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self.own_mass = 0
        self.own_amount_fans = 0
        self.own_lenght_unit = 0
        self.own_diameter_fan = 0
        self.own_spacing = 0
        self.own_fans_on_wing = 0
        self.own_fans_on_fuselage = 0
        self._freeze()

    @property
    def amount_motor(self):
        return self.own_amount_fans

    def size_self(self):
        Span = self.WingGroup.Wing.span
        V0 = self.WingGroup.Aircraft.states['cruise'].velocity
        altitude = self.WingGroup.Aircraft.states['cruise'].altitude
        Tt = self.WingGroup.Aircraft.reference_thrust
        D_fus = self.WingGroup.Aircraft.FuselageGroup.Fuselage.outer_width


        # Constants
        P_motor = self.P_motor  # power of the electric motor [W]
        specific_mass_motor_inverter = self.specific_mass_motor_inverter  # [W/kg] for the 2MW motor
        omega = self.rotational_speed_emotor
        pr = self.pressure_ratio
        flow_coef = self.flow_coef
        eff_mot_inv = self.eff_mot_inv
        propulsive_eff = self.propulsive_eff
        increase_BLI_eff = self.increase_BLI_eff
        pylon_mass_contingency = self.pylon_mass_contingency
        rho = ISA.getDensity(altitude)
        Ps = ISA.getPressure(altitude)

        ##### TODO
        length_ailerons = 0.2 * Span  # the aileron are 20 % of the total span

        # Calculations
        P_aircraft = Tt * V0
        n_fans = np.ceil(P_aircraft / (P_motor * eff_mot_inv * (propulsive_eff+increase_BLI_eff)))
        Tf = Tt / n_fans
        Pt0 = Ps + 0.5 * rho * V0 ** 2
        Pt1 = Pt0 * pr
        V1 = np.sqrt(2 * (Pt1 - Ps) / rho)
        m_dot = Tf / (V1 - V0)
        r = (m_dot / (flow_coef * rho * np.pi * omega)) ** (1 / 3)
        D_fan = 2 * r
        min_spacing = 0.07 * D_fan

        # get the weight of ducted fan
        mass_fan = 389.54 * D_fan ** 2 + 55.431 * D_fan - 2.064  # from excel regression
        vol_fan = 4.9804 * D_fan ** 2 - 4.6767 * D_fan + 1.3557
        length_fan = vol_fan / (np.pi * r ** 2)

        # TODO get weight motor + inverter
        # mass_motor_inverter =       # from email saluqi
        mass_motor_inverter = P_motor / specific_mass_motor_inverter

        # total weight of prop subsys
        mass_total = n_fans * (mass_fan + mass_motor_inverter) * pylon_mass_contingency # gearbox??

        # spacing
        if (n_fans % 2) == 0:
            n_fans_wing = n_fans
            n_fans_odd = 0
        elif (n_fans % 2) == 1:
            n_fans_wing = n_fans -1
            n_fans_odd = 1
        spacing = (Span - D_fus - 2 * length_ailerons - 2 * min_spacing - D_fan * n_fans_wing) / (n_fans_wing - 2)
        if 0 <= spacing < min_spacing:
            n_fans_fit_wing = (Span - D_fus - 2 * length_ailerons) / (D_fan + min_spacing)
            n_fans_fuselage = n_fans - n_fans_fit_wing
            self.logger.warning(f"The engines are too close together. There are {n_fans} fans but only {n_fans_fit_wing} fit in the wing. "
                                f"The number of fans on the fuselage is {n_fans_fuselage}")
        elif spacing < 0:
            n_fans_fit_wing = (Span - D_fus - 2 * length_ailerons) / (D_fan + min_spacing)
            n_fans_fuselage = n_fans - n_fans_fit_wing
            self.logger.warning(f"The engines do not fit on the wing. There are {n_fans} fans but only {n_fans_fit_wing} fit in the wing"
                                f"The number of fans on the fuselage is {n_fans_fuselage}")
        else:
            n_fans_fit_wing = n_fans_wing
            n_fans_fuselage = n_fans_odd


        self.own_mass = mass_total
        self.own_amount_fans = n_fans
        self.own_lenght_unit = length_fan
        self.own_diameter_fan = D_fan
        self.own_spacing = spacing
        self.own_fans_on_wing = n_fans_fit_wing
        self.own_fans_on_fuselage = n_fans_fuselage
        self.pos = np.array([0., 0., 0.])

    def cg_self(self):
        x_cg = 0.5 * self.WingGroup.Wing.mean_geometric_chord #TODO now they are put in the middle of the wing
        y_cg = 0
        z_cg = 0
        self.own_cg = np.array([x_cg, y_cg, z_cg])
