from detailedDesign.classes.Component import Component
import numpy as np
import misc.ISA as ISA


class Engines(Component):
    def __init__(self, WingGroup, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup
        self.parent = self.WingGroup

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self.own_mass = 0
        self.own_amount_fans = 0
        self.own_lenght_unit = 0
        self.own_diameter_fan = 0
        self.own_spacing = 0
        self.own_fans_on_wing = 0
        self.own_fans_on_fuselage = 0
        self.own_amount_motor = 0
        self.own_mass_flow = 0
        self.mass_motor_inverter = 0
        self._freeze()

    @property
    def amount_motor(self):
        return self.own_amount_fans

    def size_self(self):
        Span = self.WingGroup.Wing.span
        V0_cruise = self.WingGroup.Aircraft.states['cruise'].velocity
        V0_takeoff = self.WingGroup.Aircraft.states['take-off'].velocity
        Tt_cruise = self.WingGroup.Aircraft.reference_cruise_thrust
        Tt_takeoff = self. WingGroup.Aircraft.reference_takeoff_thrust
        #D_fus = self.WingGroup.Aircraft.FuselageGroup.Fuselage.outer_width

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
        engine_failure_contingency = self.engine_failure_contingency
        rho_cruise = self.WingGroup.Aircraft.states['cruise'].density
        Ps_cruise = self.WingGroup.Aircraft.states['cruise'].pressure
        rho_takeoff = self.WingGroup.Aircraft.states['take-off'].density
        Ps_takeoff = self.WingGroup.Aircraft.states['take-off'].pressure

        # TODO
        length_ailerons = self.WingGroup.Wing.length_ailerons  # the ailerons are a part of the total span

        # Calculations for cruise
        Tt_cruise = Tt_cruise * engine_failure_contingency
        P_aircraft_cruise = Tt_cruise * V0_cruise

        #Calculations for takeoff
        Tt_takeoff = Tt_takeoff * engine_failure_contingency
        P_aircraft_takeoff = Tt_takeoff * V0_takeoff

        if P_aircraft_cruise > P_aircraft_takeoff:
            P_aircraft = P_aircraft_cruise
            Tt = Tt_cruise
            V0 = V0_cruise
            rho = rho_cruise
            Ps = Ps_cruise
            print("Cruise power")
        elif P_aircraft_takeoff == P_aircraft_cruise:
            P_aircraft = P_aircraft_cruise
            Tt = Tt_cruise
            V0 = V0_cruise
            rho = rho_cruise
            Ps = Ps_cruise
            print("Cruise and Take-off power the same")
        else:
            P_aircraft = P_aircraft_takeoff
            Tt = Tt_takeoff
            V0 = V0_takeoff
            rho = rho_takeoff
            Ps = Ps_takeoff
            print("Take-off power")

        n_fans = np.ceil(P_aircraft / (P_motor * eff_mot_inv * (propulsive_eff + increase_BLI_eff)))
        Tf = Tt / n_fans
        Pt0 = Ps + 0.5 * rho * V0 ** 2
        Pt1 = Pt0 * pr
        V1 = np.sqrt(2 * (Pt1 - Ps) / rho)
        m_dot = Tf / (V1 - V0)
        r = (m_dot / (flow_coef * rho * np.pi * omega)) ** (1 / 3)
        D_fan = 2 * r
        min_spacing = 0.05 * D_fan

        # get the weight of ducted fan
        mass_fan = 389.54 * D_fan ** 2 + 55.431 * D_fan - 2.064  # from excel regression
        vol_fan = 4.9804 * D_fan ** 2 - 4.6767 * D_fan + 1.3557
        length_fan = vol_fan / (np.pi * r ** 2)

        # TODO get weight motor + inverter
        # mass_motor_inverter =       # from email saluqi
        self.mass_motor_inverter = P_motor / specific_mass_motor_inverter

        # total weight of prop subsys
        mass_total = n_fans * (mass_fan + self.mass_motor_inverter) * pylon_mass_contingency  # gearbox??

        spacing = (Span - 2 * length_ailerons - D_fan * n_fans) / (n_fans - 1)
        if spacing < min_spacing:
            n_fans_fit_wing = np.floor((Span - 2 * length_ailerons + min_spacing) / (D_fan + min_spacing))
            n_fans_fuselage = n_fans - n_fans_fit_wing
            self.logger.warning(f" The fans do not fit on the wingspan, the number of fans is {n_fans}."
                                f" The number of fans that fit on the wing span is {n_fans_fit_wing}. "
                                f"The fans to be placed elsewhere is {n_fans_fuselage}. ")
        else:
            self.logger.warning(f" The fans fit on the wingspan, the number of fans is {n_fans}.")
            n_fans_fit_wing = n_fans
            n_fans_fuselage = 0

        # spacing
        # print(f"Fan count: {n_fans}")
        # if (n_fans % 2) == 0:
        #     n_fans_wing = n_fans
        #     n_fans_odd = 0
        # elif (n_fans % 2) == 1:
        #     n_fans_wing = n_fans - 1
        #     n_fans_odd = 1
        # else:
        #     self.logger.warning(f"Set amount of fans on wing to zero due to bad n_fans (n_fans: {n_fans})")
        #     n_fans_wing = 0
        #     n_fans_odd = 0
        #
        # spacing = (Span - 2 * length_ailerons - 2 * min_spacing - D_fan * n_fans_wing) / (n_fans_wing - 2)
        #
        # if 0 <= spacing < min_spacing:
        #     n_fans_fit_wing = np.floor((Span - D_fus - 2 * length_ailerons) / (D_fan + min_spacing))
        #     if (n_fans_fit_wing % 2) == 1:
        #         n_fans_fit_wing = n_fans_fit_wing - 1
        #     n_fans_fuselage = n_fans - n_fans_fit_wing
        #     self.logger.warning(f"The engines are too close together. There are {n_fans} fans but only {n_fans_fit_wing} fit in the wing. "
        #                         f"The number of fans on the fuselage is {n_fans_fuselage}")
        # elif spacing < 0:
        #     n_fans_fit_wing = np.floor((Span - D_fus - 2 * length_ailerons) / (D_fan + min_spacing))
        #     if (n_fans_fit_wing % 2) == 1:
        #         n_fans_fit_wing = n_fans_fit_wing - 1
        #     n_fans_fuselage = n_fans - n_fans_fit_wing
        #     self.logger.warning(f"The engines do not fit on the wing. There are {n_fans} fans but only {n_fans_fit_wing} fit in the wing. "
        #                         f"The number of fans on the fuselage is {n_fans_fuselage}")
        # else:
        #     n_fans_fit_wing = n_fans_wing
        #     n_fans_fuselage = n_fans_odd

        self.own_mass = mass_total
        self.own_amount_fans = n_fans
        self.own_lenght_unit = length_fan
        self.own_diameter_fan = D_fan
        self.own_spacing = spacing
        self.own_fans_on_wing = n_fans_fit_wing
        self.own_fans_on_fuselage = n_fans_fuselage
        self.own_amount_motor = n_fans
        self.own_mass_flow = m_dot
        self.pos = np.array([0., 0., 0.])

    def cg_self(self):
        x_cg = 0.5 * self.WingGroup.Wing.mean_geometric_chord  # TODO now they are put in the middle of the wing
        y_cg = 0
        z_cg = 0
        self.own_cg = np.array([x_cg, y_cg, z_cg])
