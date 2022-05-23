class Component:
    def __init__(self):
        self.own_mass = 0
        self.own_cg = [0, 0, 0]
        self.components = []

    def get_mass(self):
        total_mass = self.own_mass
        for component in self.components:
            total_mass += component.get_mass()
        return total_mass

    def get_cg(self):
        # TODO
        pass
