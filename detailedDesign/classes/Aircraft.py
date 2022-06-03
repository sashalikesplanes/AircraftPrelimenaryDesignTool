from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup
import misc.constants as const
from detailedDesign.get_drag import get_drag


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
        self.mtom = 1  # Initial Value
        self.oem = None
        self.payload_mass = None
        self.thrust_over_weight = 1  # Initial Value
        self.weight_over_surface = 1  # Initial Value
        self.reference_area = None
        self.reference_thrust = None
        self.own_mass = 0

        self.name = "BoatPlane"

        # Drag states
        self.C_D_min = 0.055  # Initial Value
        self.C_D_TO = 0

        self.cruise_drag = 1250000  # needed as drag comes from previous iteration

        self._freeze()

    @property
    def fuel_mass(self):
        return self.FuselageGroup.Fuselage.FuelContainer.mass_H2

    @property
    def reserve_fuel_mass(self):
        return self.FuselageGroup.Fuselage.FuelContainer.reserve_mass_H2

    def get_sized(self):
        self.reference_area = self.mtom * const.g / self.weight_over_surface
        self.reference_thrust = self.mtom * const.g * self.thrust_over_weight

        self.logger.debug(
            f"{ self.reference_area = :.4E} m2")
        self.logger.debug(
            f"{ self.reference_thrust = :.4E} N")
        self.logger.debug(f"{ self.mtom = :.4E} kg")
        for component in self.components:
            component.get_sized()

        self.payload_mass = self.get_payload_mass()

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
        self.get_cged()
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
