import numpy as np

from detailedDesign.classes.Component import Component
from misc.unitConversions import *


class Miscellaneous(Component):
    def __init__(self, FuselageGroup, design_config):
        super().__init__(design_config)
        self.FuselageGroup = FuselageGroup
        self.parent = self.FuselageGroup

        self.W_boat = None
        self.W_AC = None
        # self.W_ele = None
        self.W_furn = None
        self.W_hyd_ele = None
        self.W_apu = None
        self.W_oxy = None
        self.W_paint = None
        self.W_crew = None
        self.W_ins = None

        self._freeze()

    def size_self(self):
        mtom = self.FuselageGroup.Aircraft.mtom
        cruise_state = self.FuselageGroup.Aircraft.states['cruise']


        # Imperial list
        W_O = kg_to_lbs(mtom)  # [lbs]
        l_FS = m_to_ft(self.FuselageGroup.Fuselage.length)  # [ft]
        b = m_to_ft(self.FuselageGroup.Aircraft.WingGroup.Wing.span)  # [ft]
        n_z = self.FuselageGroup.Aircraft.ultimate_load_factor  # [-]
        n_pax = self.FuselageGroup.Fuselage.Cabin.passenger_count  # [-]
        pilot_count = 3  # [-]
        passengers_per_flight_attendant = 50
        W_FS = kg_to_lbs(self.FuselageGroup.Fuselage.AftFuelContainer.get_mass() + self.FuselageGroup.Fuselage.ForwardFuelContainer.get_mass())  # [lbs]
        l_cabin = self.FuselageGroup.Fuselage.Cabin.length
        D_fus = self.FuselageGroup.Fuselage.outer_height

        # MDF TODO: find better one
        self.W_boat = self.FuselageGroup.Fuselage.get_mass() * 0.2

        self.W_apu = 2.2 * 0.001 * mtom

        self.W_ins = 0.347 * (mtom / 2) ** 0.555 * (cruise_state.range / 1000) ** 0.25

        # self.W_hyd = 0.015 * (mtom / 2) + 272

        something_area_fus = (np.pi * m_to_ft(l_cabin) * (0.9 * m_to_ft(D_fus)) ** 2) ** 0.7
        self.logger.debug(f"{something_area_fus = }")

        # self.W_ele = 10.8 * something_area_fus * (1 - 0.18 * something_area_fus)
        self.W_hyd_ele = 0.277 * self.FuselageGroup.Aircraft.oem ** 0.8

        self.W_AC = 14 * l_cabin ** 1.28

        self.W_oxy = 20 + 0.5 * n_pax

        self.W_paint = 0.006 * mtom

        zero_fuel_mass = mtom - self.FuselageGroup.Aircraft.fuel_mass
        self.W_furn = 0.196 * (zero_fuel_mass) ** 0.91

        self.W_crew = self.FuselageGroup.Fuselage.Cabin.mass_per_passenger * (
                    n_pax // passengers_per_flight_attendant + 1 + pilot_count)

        mass = self.W_boat + self.W_apu + self.W_ins + self.W_hyd_ele + self.W_AC + self.W_oxy + self.W_paint + self.W_crew

        self.logger.debug(f"Boat mass: {self.W_boat:.4E} [kg]")
        self.logger.debug(f"Instrument mass: {self.W_ins:.4E} [kg]")
        # self.logger.debug(f"Hydraulics mass: {self.W_hyd:.4E} [kg]")
        self.logger.debug(f"Hyd + Electrical mass: {self.W_hyd_ele:.4E} [kg]")
        self.logger.debug(f"Air conditioning mass: {self.W_AC:.4E} [kg]")
        self.logger.debug(f"Furnishing mass: {self.W_furn:.4E} [kg]")
        self.logger.debug(f"APU mass: {self.W_apu:.4E} [kg]")
        self.logger.debug(f"Oxygen system mass: {self.W_oxy:.4E} [kg]")
        self.logger.debug(f"Paint mass: {self.W_paint:.4E} [kg]")
        self.logger.debug(f"Crew mass: {self.W_crew:.4E} [kg]")




        self.own_mass = mass

    def cg_self(self):
        # Position of the centre of the fuselage
        pos_centre = self.FuselageGroup.Fuselage.own_cg
        pos_cabin = self.FuselageGroup.Fuselage.Cabin.own_cg + self.FuselageGroup.Fuselage.Cabin.pos

        # TODO: check things with "???" above them
        # Makes sense to be on the same x as the centre
        pos_w_boat = pos_centre.copy()
        # further down than centre of fuselage structure
        pos_w_boat[2] = self.FuselageGroup.Fuselage.outer_height / 3
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
        cg_pos += pos_w_flight_controls * self.W_ins
        cg_pos += pos_w_hydraulics * self.W_hyd_ele
        # cg_pos += pos_w_electrical * self.W_ele
        cg_pos += pos_w_ac * self.W_AC
        cg_pos += pos_w_furnishing * self.W_furn
        cg_pos += pos_w_apu * self.W_apu
        cg_pos += pos_w_oxy * self.W_oxy
        cg_pos += pos_w_paint * self.W_paint
        cg_pos += pos_w_crew * self.W_crew

        self.own_cg = cg_pos / mass
        return self.own_cg

    @property
    def length(self):
        return self.FuselageGroup.Fuselage.length