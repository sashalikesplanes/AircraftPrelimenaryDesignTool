from detailedDesign.classes.Component import Component


class template(Component):
    def __init__(self, config):
        # Please pass my_config to any sub components as the second arg
        my_config = super().__init__(config)

        # Create all the parameters that this component must have here:
        # Using self.property_name = value
        self._freeze()
