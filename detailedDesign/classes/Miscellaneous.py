from detailedDesign.classes.Component import Component
from misc.unitConversions import *
from misc.ISA import getSpeedOfSound


class Miscellaneous(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)
        self.FuselageGroup = FuselageGroup

        self._freeze()

    def size_self(self):
        mtom = self.FuselageGroup.Aircraft.mtom

        # Imperial list
        W_O = kg_to_lbs(mtom)  # [lbs]
        l_FS = m_to_ft(self.FuselageGroup.Fuselage.length)  # [ft]
        b = m_to_ft(self.FuselageGroup.Aircraft.WingGroup.Wing.span)  # [ft]
        n_z = self.FuselageGroup.Aircraft.ultimate_load_factor  # [-]
        n_pax = self.FuselageGroup.Fuselage.Cabin.passengers  # [-]
        pilot_count = 3  # [-]
        N_OCC = n_pax + n_pax % 50 + 1 + pilot_count  # [-]
        # This needs to be in meters since the mach number requires metric units for speed of sound
        h = self.FuselageGroup.Aircraft.states["cruise"].altitude  # [m]
        M = self.FuselageGroup.Aircraft.states["cruise"].velocity / getSpeedOfSound(h)  # [-]
        W_FS = kg_to_lbs(self.FuselageGroup.Fuselage.FuelContainer.get_mass())  # [lbs]

        # MAGICAL DISNEY NUMBER WARNING (MDN)
        W_UAV = 420  # [lbs]

        # MAGICAL DISNEY FACTOR (MDF)
        W_boat = self.FuselageGroup.Fuselage.get_mass() * 0.2

        W_flight_control_system = 0.053 * l_FS ** 1.536 * b ** 0.371 * (n_z * W_O * 10 ** -4) ** 0.8

        W_hydraulics = 0.001 * W_O

        W_avionics = 2.117 * W_UAV ** 0.933

        W_electrical = 12.57 * (W_FS + W_avionics) ** 0.51

        W_AC = 0.265 * W_O ** 0.52 * N_OCC ** 0.68 * W_avionics ** 0.17 * M ** 0.08

        W_furnishing = 0.0582 * W_O - 65

        mass = W_furnishing + W_AC + W_electrical + W_avionics + W_hydraulics + W_flight_control_system + W_boat
        mass = lbs_to_kg(mass)
        self.own_mass = mass
