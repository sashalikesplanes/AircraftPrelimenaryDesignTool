import imp
from detailedDesign.classes.Component import Component
from detailedDesign.classes.FuselageGroup import FuselageGroup
from detailedDesign.classes.WingGroup import WingGroup
import misc.constants as const
from detailedDesign.get_drag import get_drag


class Aircraft(Component):
    def __init__(self, design_config, states_dict):
        super().__init__(design_config)

        self.WingGroup = WingGroup(self, self.design_config)
        self.FuselageGroup = FuselageGroup(self, self.design_config)
        self.components = [self.WingGroup, self.FuselageGroup]

        # FAKE REFERENCE AREA FOR TESTING PURPOSES
        self.reference_area = 500
        # REMOVE BECAUSE MAGICAL DISNEY VALUE
        self.states = states_dict

        # Create all the parameters that this component must have here:
        # Use self.property = None
        self.mtom = None
        self.oem = None
        self.fuel_mass = None
        self.thrust_over_weight = None
        self.weight_over_surface = None
        self.reference_area = None
        self.reference_thrust = None

        # Drag states
        self.C_D_min = None
        self.C_L_max = None

        self._freeze()

    def size_self(self):
        self.reference_area = self.mtom * const.g / self.weight_over_surface
        self.reference_thrust = self.mtom * const.g * self.thrust_over_weight

        self.oem = self.get_mass()

        drag, CDs = get_drag(self)
        # Update CDmin
