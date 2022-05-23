# To Check
from detailedDesign.classes.Component import Component


class Engines(Component):
    def __init__(self, WingGroup, config):
        my_config = super().__init__(config)
        self.WingGroup = WingGroup
        self.count = 69
