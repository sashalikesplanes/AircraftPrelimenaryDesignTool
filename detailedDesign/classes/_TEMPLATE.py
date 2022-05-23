from detailedDesign.classes.Component import Component


class template(Component):
    def __init__(self, ParentComponent, design_config):
        super().__init__(design_config)

        # Save reference to be able to reach parent
        self.ParentComponent = ParentComponent

        self.components = []  # List of all child components

        # Create all the parameters that this component must have here:
        # Using self.property_name = None
        self.example_property = None

        self._freeze()  # Last line
