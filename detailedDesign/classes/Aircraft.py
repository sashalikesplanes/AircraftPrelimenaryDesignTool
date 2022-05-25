import imp
from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup
import misc.constants as const
from detailedDesign.get_drag import get_drag


class Aircraft(Component):
    def __init__(self, design_config, states_dict):
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
        self.fuel_mass = 0
        self.payload_mass = None
        self.thrust_over_weight = 1  # Initial Value
        self.weight_over_surface = 1  # Initial Value
        self.reference_area = None
        self.reference_thrust = None

        # Drag states
        self.C_D_min = 0.1  # Initial Value

        self.ultimate_load_factor = None
        self.clean_stall_speed = None
        self.cruise_drag = None

        self._freeze()

    def get_sized(self):
        # TODO Calculate payload mass
        self.reference_area = self.mtom * const.g / self.weight_over_surface
        self.reference_thrust = self.mtom * const.g * self.thrust_over_weight

        for component in self.components:
            component.get_sized()

        self.payload_mass = self.get_payload_mass()

        self.oem = self.get_mass()

        total_C_D_min, CDi, CD, total_drag = get_drag(self)
        self.C_D_min = total_C_D_min
        self.cruise_drag = total_drag

        self.mtom = self.oem + self.payload_mass + self.fuel_mass

    def get_payload_mass(self):
        # Right now only count passengers. Their mass includes their luggage
        num_of_pax = self.FuselageGroup.Fuselage.Cabin.passengers
        mass_per_pax = self.FuselageGroup.Fuselage.Cabin.mass_per_passenger

        return num_of_pax * mass_per_pax
