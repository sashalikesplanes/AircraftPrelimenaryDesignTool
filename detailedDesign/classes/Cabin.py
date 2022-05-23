import numpy as np

from detailedDesign.classes.Component import Component


class Cabin(Component):
    def __init__(self, Fuselage, config):
        my_config = super().__init__(config)
        self.Fuselage = Fuselage
        self.config = my_config
        self.max_seats_abreast = my_config["max_seats_abreast"]
        self.max_rows_per_floor = my_config["max_rows_per_floor"]

        # This list could be used later to load the passengers for the cg range diagram
        self.components = []

        # Create all the parameters that this component must have here:
        # Using self.property_name = value

        self.seats_abreast = None
        self.floor_count = None
        self.rows_per_floor = None
        self.aisle_count = None

        self.passengers = my_config["passengers"]

        self.height = None
        self.width = None
        self.length = None
        self.diameter = None

        self._freeze()

    def size_self(self):
        """Function to size the cabin"""
        # TODO: improve model to work better with circular fuselages
        # Do stuff
        n_floors = 1
        n_pax = self.passengers
        # ADSEE I formula for seats abreast
        n_sa = np.ceil(0.45 * n_pax ** 0.5)

        # If the maximum seats abreast is reached we will decrease the number to the maximum allowed
        if n_sa > self.max_seats_abreast:
            n_sa = self.max_seats_abreast

        # Get the amount of aisles while preventing more than 4 seats needing to be placed
        # next to one another.
        if n_sa <= 6:
            n_aisles = 1
        else:
            n_aisles = np.ceil(n_sa - 6) / 4 + 1

        # Calculate the amount of rows for the case where there is only one floor
        n_rows = np.ceil(n_pax / n_sa)

        # find the amount of floors which satisfies the maximum rows in a floor
        while n_rows / n_floors > self.max_rows_per_floor:
            n_floors += 1

        # Calculate the average rows per floor
        n_rows = np.ceil(n_rows / n_floors)

        # Save seating arrangement into the object
        self.seats_abreast = n_sa
        self.rows_per_floor = n_rows
        self.floor_count = n_floors
        self.aisle_count = n_aisles

        # Calculate the dimensions of the rectangular cabin
        self.height = n_floors * self.config["floor_height"]
        self.width = n_sa * \
            self.config["seat_width"] + n_aisles * self.config["aisle_width"]
        self.length = n_rows * self.config["k_cabin"]
        # Find the diameter of the cabin using the width and the height and the smallest circle
        self.diameter = 2 * ((0.5 * self.width) ** 2 +
                             (0.5 * self.height) ** 2) ** 0.5

        # Debug print statements
        # print(self.height, self.width, self.length)
        # print(self.diameter)
        # print(self.height * self.width * self.length)
