from detailedDesign.classes.Component import Component
from misc.unitConversions import *
from misc.ISA import getSpeedOfSound


class Miscellaneous(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)
        self.FuselageGroup = FuselageGroup

        self.W_boat = None
        self.W_avionics = None
        self.W_AC = None
        self.W_electrical = None
        self.W_furnishing = None
        self.W_hydraulics = None
        self.W_flight_control_system = None

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
        passengers_per_flight_attendent = 50
        N_OCC = n_pax + n_pax // passengers_per_flight_attendent + 1 + pilot_count  # [-]
        # This needs to be in meters since the mach number requires metric units for speed of sound
        h = self.FuselageGroup.Aircraft.states["cruise"].altitude  # [m]
        # [-]
        M = self.FuselageGroup.Aircraft.states["cruise"].velocity / \
            getSpeedOfSound(h)
        W_FS = kg_to_lbs(
            self.FuselageGroup.Fuselage.FuelContainer.get_mass())  # [lbs]

        # MAGICAL DISNEY NUMBER WARNING (MDN)
        W_UAV = 420  # [lbs]

        # MAGICAL DISNEY FACTOR (MDF)
        self.W_boat = self.FuselageGroup.Fuselage.get_mass() * 0.2

        self.W_flight_control_system = lbs_to_kg(
            0.053 * l_FS ** 1.536 * b ** 0.371 * (n_z * W_O * 10 ** -4) ** 0.8)

        self.W_hydraulics = lbs_to_kg(0.001 * W_O)

        self.W_avionics = lbs_to_kg(2.117 * W_UAV ** 0.933)

        self.W_electrical = lbs_to_kg(
            12.57 * (W_FS + kg_to_lbs(self.W_avionics)) ** 0.51)

        # self.W_AC = lbs_to_kg(0.265 * W_O ** 0.52 * N_OCC **
        #                       0.68 * kg_to_lbs(self.W_avionics) ** 0.17 * M ** 0.08)

        self.W_AC = lbs_to_kg(14 * m_to_ft(self.FuselageGroup.Fuselage.Cabin.length) **1.28)

        self.W_furnishing = lbs_to_kg(0.0582 * W_O - 65)

        # self.W_apu = lbs_to_kg(2.2 * 0.001 * W_O

        self.logger.debug(f"Boat mass: {self.W_boat:.4E} [kg]")
        self.logger.debug(
            f"Flight control system mass: {self.W_flight_control_system:.4E} [kg]")
        self.logger.debug(f"Hydraulics mass: {self.W_hydraulics:.4E} [kg]")
        self.logger.debug(f"Avionics mass: {self.W_avionics:.4E} [kg]")
        self.logger.debug(f"Electrical mass: {self.W_electrical:.4E} [kg]")
        self.logger.debug(f"Air conditioning mass: {self.W_AC:.4E} [kg]")
        self.logger.debug(f"Furnishing mass: {self.W_furnishing:.4E} [kg]")
        mass = self.W_furnishing + self.W_AC + self.W_electrical + self.W_avionics + \
            self.W_hydraulics + self.W_flight_control_system + self.W_boat
        self.own_mass = mass
