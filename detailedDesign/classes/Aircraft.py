from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup
from detailedDesign.board_passengers import board_passengers, unboard_passengers_fuel, board_passengers_half_fuel
import misc.constants as const
from detailedDesign.get_drag import get_drag
import numpy as np


class Aircraft(Component):
    def __init__(self, design_config, states_dict, debug=True):
        super().__init__(design_config)

        del self.own_mass  # Not needed as Aircraft has no additional mass itself

        self.WingGroup = WingGroup(self, self.design_config)
        self.FuselageGroup = FuselageGroup(self, self.design_config)
        self.components = [self.WingGroup, self.FuselageGroup]

        self.states = states_dict

        # Create all the parameters that this component must have here:
        # Use self.property = None
        self.mtom = 2  # Initial Value
        self.oem = 1
        self.payload_mass = None
        self.thrust_over_weight_cruise = 0.1  # Initial Value
        self.thrust_over_weight_takeoff = 0.1
        self.weight_over_surface = 1  # Initial Value
        self.reference_area = None
        self.reference_cruise_thrust = None
        self.reference_takeoff_thrust = None
        self.own_mass = 0

        self.name = "BoatPlane"

        # Drag states
        self.C_D_min = 0.055  # Initial Value
        self.C_D_TO = 0

        self.cruise_drag = 750000  # needed as drag comes from previous iteration

        self._freeze()

    @property
    def fuel_mass(self):
        return self.FuselageGroup.Power.mass_H2

    @property
    def zero_fuel_mass(self):
        return self.oem + self.get_payload_mass + self.cargo_mass

    @property
    def reserve_fuel_mass(self):
        return self.FuselageGroup.Fuselage.FuelContainer.reserve_mass_H2

    @property
    def C_m_alpha(self):
        x_cg = self.cg_loaded_half_fuel[0]
        x_acw = self.FuselageGroup.Tail.HorizontalTail.x_aerodynamic_center
        x_ach = self.WingGroup.Wing.x_aerodynamic_center
        horizontal_tail_ratio = self.FuselageGroup.Tail.HorizontalTail.surface_area / self.WingGroup.Wing.wing_area
        C_L_H_alpha = np.rad2deg(self.FuselageGroup.Tail.HorizontalTail.C_L_alpha)
        print('',end="\n\n\n\n\n\n")
        print(C_L_H_alpha)
        C_m_alpha_fus = self.FuselageGroup.Fuselage.C_m
        print(C_m_alpha_fus)
        d_alphah_d_alpha = self.FuselageGroup.Tail.HorizontalTail.d_alphah_d_alpha
        mean_geometric_chord_wing = self.WingGroup.Wing.mean_geometric_chord
        C_L_term = np.rad2deg(self.WingGroup.Wing.C_L_alpha) * (x_cg - x_acw) / mean_geometric_chord_wing
        print(np.rad2deg(self.WingGroup.Wing.C_L_alpha))
        print('',end="\n\n\n\n\n\n")
        C_L_H_term = 0.9 * horizontal_tail_ratio * C_L_H_alpha * d_alphah_d_alpha * (x_ach - x_cg) / mean_geometric_chord_wing
        return C_L_term + C_m_alpha_fus - C_L_H_term

    @property
    def neutral_point(self):
        C_m_alpha = self.C_m_alpha
        C_L_alpha = np.rad2deg(self.WingGroup.Wing.C_L_alpha)
        mean_geometric_chord_wing = self.WingGroup.Wing.mean_geometric_chord
        x_cg = self.cg_loaded_half_fuel[0] / mean_geometric_chord_wing
        return  (- C_m_alpha / C_L_alpha + x_cg) * mean_geometric_chord_wing

    def get_sized(self):
        self.reference_area = self.mtom * const.g / self.weight_over_surface
        self.reference_cruise_thrust = self.mtom * const.g * self.thrust_over_weight_cruise
        self.reference_takeoff_thrust = self.mtom * const.g * self.thrust_over_weight_takeoff

        self.logger.debug(
            f"{ self.reference_area = :.4E} m2")
        self.logger.debug(f"{ self.mtom = :.4E} kg")
        for component in self.components:
            component.get_sized()

        self.payload_mass = self.get_payload_mass

        self.oem = self.get_mass() * self.oem_contingency

        total_C_D_min, CDi, CD, total_drag, self.C_D_TO = get_drag(self)
        self.C_D_min = total_C_D_min
        self.cruise_drag = total_drag
        self.logger.debug(f"DRAG: { self.C_D_min = } [-], { self.cruise_drag = } N")

        new_mtom = self.oem + self.payload_mass + self.fuel_mass + self.cargo_mass
        # Take a weighted average to prevent oscillations
        # self.mtom = (new_mtom * 0.1 + self.mtom * 0.9) 
        self.mtom = new_mtom
        self.print_component_masses()

    @property
    def get_payload_mass(self):
        # Right now only count passengers. Their mass includes their luggage
        num_of_pax = self.FuselageGroup.Fuselage.Cabin.passenger_count
        mass_per_pax = self.FuselageGroup.Fuselage.Cabin.mass_per_passenger

        return num_of_pax * mass_per_pax

    @property
    def fuel_mass(self):
        return self.FuselageGroup.Power.mass_H2

    @property
    def oew(self):
        return self.oem

    def get_cg(self):
        """Calculate the cg of this component and all its sub-components"""
        # self.get_cged()
        total_mass_factor = self.own_mass
        cg_pos = self.own_cg * self.own_mass

        for component in self.components:
            cg_pos += (component.get_cg() + component.pos) * component.get_mass()
            total_mass_factor += component.get_mass()

        if total_mass_factor != 0:
            cg_pos = cg_pos / total_mass_factor
        else:
            cg_pos = self.own_cg

        return cg_pos

    @property
    def cg_empty(self):
        """Get cg of empty aircraft with all the components"""
        self.get_cged()
        return self.get_cg()

    @property
    def cg_loaded(self):
        """Get cg of the whole aircraft with passengers and fuel loaded and all the pre calcs"""
        board_passengers(self)
        self.get_cged()
        cg = self.get_cg()
        unboard_passengers_fuel(self)
        return cg

    @property
    def cg_loaded_half_fuel(self):
        """GEt cg of AC with pax and half the fuel in each tank"""
        board_passengers_half_fuel(self)
        self.get_cged()
        cg = self.get_cg()
        unboard_passengers_fuel(self)
        return cg

    @property
    def takeoff_speed(self): 
        return np.sqrt(self.mtom * 9.81 / (0.5 * 1.225 * self.reference_area * self.C_L_TO))

    def plot_cgs(self):
        self.get_cged()
        lst = []
        for component in self.components:
            new_lst = component.plot_cgs()
            for i in range(len(new_lst)):
                # print(new_lst[i][0], component.pos)
                new_lst[i][0] = component.pos + new_lst[i][0]
                # print(new_lst[i])
            lst += new_lst

        lst.append([self.own_cg, f"{str(self)}"])
        return lst

    @property
    def transformed_pos(self):
        return self.pos
