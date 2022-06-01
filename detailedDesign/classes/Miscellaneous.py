import numpy as np

from detailedDesign.classes.Component import Component
from misc.unitConversions import *


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
        self.W_apu = None
        self.W_oxy = None
        self.W_paint = None
        self.W_crew = None

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
        passengers_per_flight_attendant = 50
        W_FS = kg_to_lbs(self.FuselageGroup.Fuselage.FuelContainer.get_mass())  # [lbs]

        # MDN
        W_UAV = 2000  # [lbs]

        # MDF TODO: find better one
        self.W_boat = self.FuselageGroup.Fuselage.get_mass() * 0.2

        self.W_flight_control_system = lbs_to_kg(
            0.053 * l_FS ** 1.536 * b ** 0.371 * (n_z * W_O * 10 ** -4) ** 0.8)

        self.W_hydraulics = lbs_to_kg(0.001 * W_O)

        self.W_avionics = lbs_to_kg(2.117 * W_UAV ** 0.933)

        self.W_electrical = lbs_to_kg(
            12.57 * (W_FS + kg_to_lbs(self.W_avionics)) ** 0.51)

        self.W_AC = lbs_to_kg(14 * m_to_ft(self.FuselageGroup.Fuselage.Cabin.length) ** 1.28)

        self.W_furnishing = lbs_to_kg(0.0582 * W_O - 65)

        self.W_apu = lbs_to_kg(2.2 * 0.001 * W_O)

        self.W_oxy = lbs_to_kg(40 + 2.4 * n_pax)

        self.W_paint = 0.006 * mtom

        self.W_crew = self.FuselageGroup.Fuselage.Cabin.mass_per_passenger * (
                    n_pax // passengers_per_flight_attendant + 1 + pilot_count)

        self.logger.debug(f"Boat mass: {self.W_boat:.4E} [kg]")
        self.logger.debug(f"Flight control system mass: {self.W_flight_control_system:.4E} [kg]")
        self.logger.debug(f"Hydraulics mass: {self.W_hydraulics:.4E} [kg]")
        self.logger.debug(f"Avionics mass: {self.W_avionics:.4E} [kg]")
        self.logger.debug(f"Electrical mass: {self.W_electrical:.4E} [kg]")
        self.logger.debug(f"Air conditioning mass: {self.W_AC:.4E} [kg]")
        self.logger.debug(f"Furnishing mass: {self.W_furnishing:.4E} [kg]")
        self.logger.debug(f"APU mass: {self.W_apu:.4E} [kg]")
        self.logger.debug(f"Oxygen system mass: {self.W_oxy:.4E} [kg]")
        self.logger.debug(f"Paint mass: {self.W_paint:.4E} [kg]")
        self.logger.debug(f"Crew mass: {self.W_crew:.4E} [kg]")

        mass = self.W_furnishing + self.W_AC + self.W_electrical + self.W_avionics + \
               self.W_hydraulics + self.W_flight_control_system + self.W_boat + self.W_apu + self.W_oxy + self.W_crew
        self.own_mass = mass

    def cg_self(self):
        # Position of the centre of the fuselage
        pos_centre = self.FuselageGroup.Fuselage.own_cg
        pos_cabin = self.FuselageGroup.Fuselage.Cabin.own_cg + self.FuselageGroup.Fuselage.Cabin.pos

        # TODO: check things with "???" above them
        # Makes sense to be on the same x as the centre
        pos_w_boat = pos_centre.copy()
        # further down than centre of fuselage structure
        pos_w_boat[2] = self.FuselageGroup.Fuselage.outer_diameter / 3
        # in the cockpit
        pos_w_flight_controls = pos_centre
        # pos_w_flight_controls = np.array([0.5 * self.FuselageGroup.Fuselage.cockpit_length, 0., -0.25 * self.FuselageGroup.Fuselage.outer_diameter])
        # ???
        pos_w_hydraulics = pos_centre
        # ???
        pos_w_avionics = pos_centre
        # Makes sense to put in centre
        pos_w_electrical = pos_centre
        # in the middle of cabin
        pos_w_ac = pos_cabin
        # in the middle of cabin
        pos_w_furnishing = pos_cabin
        # put it in the back of the tail
        pos_w_apu = np.array([self.FuselageGroup.Fuselage.length * 0.9, 0., 0.])
        # ???
        pos_w_oxy = pos_centre
        # same cg as fuselage structure
        pos_w_paint = pos_centre
        # in the centre of the cabin
        pos_w_crew = pos_cabin

        mass = self.own_mass

        cg_pos = pos_w_boat * self.W_boat
        cg_pos += pos_w_flight_controls * self.W_flight_control_system
        cg_pos += pos_w_hydraulics * self.W_hydraulics
        cg_pos += pos_w_avionics * self.W_avionics
        cg_pos += pos_w_electrical * self.W_electrical
        cg_pos += pos_w_ac * self.W_AC
        cg_pos += pos_w_furnishing * self.W_furnishing
        cg_pos += pos_w_apu * self.W_apu
        cg_pos += pos_w_oxy * self.W_oxy
        cg_pos += pos_w_paint * self.W_paint
        cg_pos += pos_w_crew * self.W_crew
        return cg_pos / mass

