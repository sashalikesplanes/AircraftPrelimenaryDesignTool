# To check
from Component import Component

class Batteries(Component):
    def __init__(self, Power):
        super().__init__()
        self.Power = Power