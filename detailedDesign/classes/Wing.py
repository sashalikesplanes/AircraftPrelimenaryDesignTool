# To Check
from detailedDesign.classes.Component import Component
from detailedDesign.classes.HLDs import HLDs


class Wing(Component):
    def __init__(self, WingGroup, design_config):
        super().__init__(design_config)

        self.WingGroup = WingGroup
        self.HLDs = HLDs(self, self.design_config)
        self.components = [self.HLDs]

        self.wing_area = None
        self.span = None
        self.tip_chord = None
        self.root_chord = None

        # Create all the parameters that this component must have here:
        # Using self.property_name = None
        self._freeze()

    def size_self(self):
        self.wing_area = self.WingGroup.Aircraft.reference_area

        self.span = (self.wing_area * self.aspect_ratio) ** 0.5
        print(self.span)
        self.root_chord = (2 * self.wing_area) / (self.span * (1 + self.taper_ratio))
        self.tip_chord = self.root_chord * self.taper_ratio
        print(self.root_chord, self.tip_chord)
