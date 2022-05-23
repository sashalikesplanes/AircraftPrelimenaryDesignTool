import imp
from Component import Component


class WingGroup(Component):
    def __init__(self, Aircraft):
        super().__init__()
        self.Aircraft = Aircraft
