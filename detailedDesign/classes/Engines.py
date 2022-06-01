# To Check
from detailedDesign.classes.Component import Component
import numpy as np


class Engines(Component):
    def __init__(self, WingGroup, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self.volume = 0
        self.own_total_mass = 0
        self.own_amount_prop = 0
        self.own_lenght_unit = 0
        self.own_width_unit = 0
        self.own_height_unit = 0
        self.own_amount_motor = None

        self._freeze()

    @property
    def amount_motor(self):
        return self.own_amount_motor

    def size_self(self):
        S = self.WingGroup.Wing.span
        V = self.WingGroup.Aircraft.states['cruise'].velocity
        range = self.WingGroup.Aircraft.states['cruise'].range
        T = self.WingGroup.Aircraft.reference_thrust
        D_fus = self.WingGroup.Aircraft.FuselageGroup.Fuselage.outer_diameter

        # Ref aircraft An-22 data
        P_eng = self.P_eng_an22  # [W] Power of one engine of the An-22
        D_prop_an22 = self.D_prop_an22  # [m] diameter of propeller of An-22

        # Constants
        P_motor = self.P_motor  # power of the electric motor [W]
        m_specific_motor = self.m_specific_motor  # [W/kg] for the 2MW motor
        # [m] diameter of the 2MW motor using the coca-cola method
        d_motor = self.d_motor
        l_motor = self.l_motor  # [m] length of a motor
        clearance = self.clearance  # distance between fuselage and engine from literature
        m_propeller = self.m_propellor  # [kg] from the excel extrapolation
        l_inverter = self.l_inverter
        m_specific_inverter = self.m_specific_inverter
        vol_specific_inverter = self.vol_specific_inverter

        # Contingencies and efficiencies
        eff_gearbox = self.eff_gearbox  # efficiency of a gearbox connection
        spacing_motor_contingency = self.spacing_motor_contingency
        height_unit_contingency = self.height_unit_contingency
        gearbox_unit_vol_contingency = self.gearbox_unit_vol_contingency
        gearbox_unit_mass_contingency = self.gearbox_unit_mass_contingency
        width_gearbox_contingency = self.width_gearbox_contingency

        # Calculations
        P_aircraft = T * V  # power the aircraft needs  [W]
        # amount of motors per propellor
        group = np.ceil(P_eng / (P_motor * eff_gearbox))
        n_prop = np.ceil(P_aircraft / P_eng)
        n_motor = group * n_prop
        # n_prop = np.ceil((P_aircraft/P_eng)/2)*2    # we want an even number of propelors
        # n_motor = np.ceil((group * n_prop)/2)*2

        length_unit = np.ceil(
            group / 2) * d_motor * spacing_motor_contingency  # [m] asuming they are connected in series
        width_unit = 2 * (l_motor + l_inverter) * width_gearbox_contingency
        height_unit = d_motor * height_unit_contingency

        S_fit = (n_prop-1) * D_prop_an22 + 2 * clearance + (1 / 3) * D_prop_an22 * (
            n_prop - 2) + D_fus  # ideal span to fit all propellers needed
        n_prop_fit = np.floor((S - 2 * clearance - D_fus + (2 / 3) * D_prop_an22) / (
            (4 / 3) * D_prop_an22))  # amount of propellers needed to fit in the desired span

        if S_fit > S:
            self.logger.warning(
                f"The propellers don't fit in the Span. The span should be at least {S_fit} but it is {S}. The maximum amount of propellors that fit is {n_prop_fit}")

        d_max_prop = (S - D_fus - 2 * clearance) / (
            (4 / 3) * n_prop - (2 / 3))  # from the geometry with spacing of 1/3 of d_prop

        # mass of the motors needed to produce the thrust
        m_motor = P_motor / m_specific_motor
        vol_motor = d_motor * d_motor * l_motor  # [m3]
        # the volume is calculated as if the motor had a box like shape
        # instead of being a cylinder

        m_inverter = P_motor / m_specific_inverter
        vol_inverter = P_motor / vol_specific_inverter

        vol_unit = group * (vol_motor + vol_inverter) * \
            gearbox_unit_vol_contingency
        vol_total = n_prop * vol_unit
        m_unit = ((m_motor + m_inverter) * group + m_propeller) * \
            gearbox_unit_mass_contingency
        m_total = n_prop * m_unit

        self.own_mass = m_total
        self.own_amount_prop = n_prop
        self.own_lenght_unit = length_unit
        self.own_width_unit = width_unit
        self.own_height_unit = height_unit
        self.own_amount_motor = n_motor
