import numpy as np
from detailedDesign.classes.Component import Component


class Cabin(Component):
    def __init__(self, Fuselage, design_config):
        super().__init__(design_config)
        self.Fuselage = Fuselage
        self.parent = self.Fuselage
        # self.config = my_config
        # self.max_seats_abreast = my_config["max_seats_abreast"]
        # self.max_rows_per_floor = my_config["max_rows_per_floor"]

        # This list could be used later to load the passengers for the cg range diagram
        self.components = []

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self.rows_per_floor = None

        self.passengers = []

        self._freeze()

    def size_self(self):
        """Function to size the cabin"""
        # TODO Fix Position

        # Do stuff
        # n_floors = 1
        n_pax = self.passenger_count
        # ADSEE I formula for seats abreast
        # n_sa = np.ceil(0.45 * n_pax ** 0.5)

        # If the maximum seats abreast is reached we will decrease the number to the maximum allowed
        # if n_sa > self.max_seats_abreast:
        #    n_sa = self.max_seats_abreast

        # Calculate the amount of rows for the case where there is only one floor
        # n_rows = np.ceil(n_pax / n_sa)

        # find the amount of floors which satisfies the maximum rows in a floor
        # while n_rows / n_floors > self.max_rows_per_floor:
        #     n_floors += 1

        # # Calculate the average rows per floor
        # n_rows = np.ceil(n_rows / n_floors)

        # Save seating arrangement into the object
        n_rows = np.ceil(n_pax / (self.floor_count * self.seats_abreast))
        self.rows_per_floor = n_rows

        # Calculate the dimensions of the rectangular cabin
        # This is now done using properties because cool

        # Debug statements
        self.logger.debug(f"height x width x length: ({self.height:.4E} {self.width:.4E} {self.length:.4E}) [m]")
        self.logger.debug(f"Cabin volume: {self.height * self.width * self.length:.4E} [m3]")
        self.pos = np.array([self.Fuselage.cockpit_length, 0., self.z_offset])

    @property
    def height(self):
        return self.floor_count * self.floor_height

    @property
    def width(self):
        return self.seats_abreast * self.seat_width + self.aisle_count * self.aisle_width

    @property
    def length(self):
        return self.rows_per_floor * self.k_cabin

    def cg_self(self):
        x_cg = self.length * 0.5
        # Assume that the zero point goes through the centre of the cylindrical fuselage
        y_cg = 0
        z_cg = 0
        self.own_cg = np.array([x_cg, y_cg, z_cg])

    def get_cg(self):
        """Calculate the cg of this component and all its sub-components"""
        total_mass_factor = self.own_mass
        cg_pos = self.own_cg * self.own_mass

        for passenger in self.passengers:
            cg_pos += passenger.pos * passenger.mass
            total_mass_factor += passenger.mass

        for component in self.components:
            cg_pos += (component.get_cg() + component.pos) * component.get_mass()
            total_mass_factor += component.get_mass()

        if total_mass_factor != 0:
            cg_pos = cg_pos / total_mass_factor
        else:
            cg_pos = self.own_cg

        return cg_pos

    def get_mass(self):
        mass = 0

        for passenger in self.passengers:
            mass += passenger.mass

        return mass
