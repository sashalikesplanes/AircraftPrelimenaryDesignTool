# To Check
from detailedDesign.classes.Component import Component


class HLDs(Component):
    def __init__(self, Wing, config):
        my_config = super().__init__(config)
        self.Wing = Wing
