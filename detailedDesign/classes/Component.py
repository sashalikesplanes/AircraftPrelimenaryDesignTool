class Component():
    def __init__(self, config):
        self.own_mass = 0
        self.own_cg = [0, 0, 0]
        self.components = []

        my_config = config[type(self).__name__]

        for prop in my_config:
            if type(my_config[prop]).__name__ != 'dict':
                setattr(self, prop, my_config[prop])

        return my_config

    def get_mass(self):
        total_mass = self.own_mass
        for component in self.components:
            total_mass += component.get_mass()
        return total_mass

    def get_cg(self):
        # TODO
        pass

    def get_sized(self):
        raise ValueError("I AM NOT SIZED RIGHT")
