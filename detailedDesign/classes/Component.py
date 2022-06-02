import logging
import numpy as np


class Component:

    # Used to mark the Component to not allow properties to be added
    __is_frozen = False

    def __init__(self, design_config):
        self.own_mass = 0
        self.own_cg = np.array([0., 0., 0.])
        self.pos = np.array([0., 0., 0.])
        self.components = []

        self.logger = logging.getLogger("logger")
        self.design_config = self.unwrap_design_config(design_config)

        for prop in self.design_config:
            if type(self.design_config[prop]).__name__ != 'dict':
                setattr(self, prop, self.design_config[prop])

    def get_mass(self):
        total_mass = self.own_mass
        for component in self.components:
            total_mass += component.get_mass()
        return total_mass

    def get_cg(self):
        """Calculate the cg of this component and all its sub-components"""
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

    def size_self(self):
        self.logger.warning(f"{self} is not being sized")

    def cg_self(self):
        """Calculate this parts cg for later usage"""
        if self.own_mass != 0:
            self.logger.warning(f"{self} is not being cged")

    def get_cged(self):
        """Make the components calculate their individual cg"""
        self.cg_self()

        for component in self.components:
            component.get_cged()

    def get_sized(self):
        """Size the component based on actual values"""
        self.size_self()

        for component in self.components:
            component.get_sized()

    # Recursively print the masses of all the components
    def print_component_masses(self, prev_mass=None, depth=0):
        if prev_mass:
            percent_mass = self.get_mass() / prev_mass * 100
        else:
            percent_mass = 100

        self.logger.debug(f"{' ' * depth * 2}{type(self).__name__:<15}{self.get_mass():<20.4E}[kg]{percent_mass:>20.2f} %")
        for component in self.components:
            component.print_component_masses(prev_mass=self.get_mass(), depth=depth+1)

    def unwrap_design_config(self, design_config):
        return design_config[type(self).__name__]

    def __setattr__(self, key, value):
        if self.__is_frozen and not hasattr(self, key):
            raise TypeError(
                "%r, you cannot add new properties. Please first define it in the class __init__" % self)
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__is_frozen = True

    def __str__(self):
        return type(self).__name__
