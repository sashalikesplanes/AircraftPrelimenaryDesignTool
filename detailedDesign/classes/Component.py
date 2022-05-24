class Component:

    # Used to mark the Component to not allow properties to be added
    __is_frozen = False

    def __init__(self, design_config):
        self.own_mass = 0
        self.own_cg = [0, 0, 0]
        self.components = []

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
        # TODO
        pass

    def size_self(self):
        print(f"WARNING! {self} IS NOT BEING SIZE")

    def get_sized(self):
        self.size_self()

        for component in self.components:
            component.get_sized()

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
