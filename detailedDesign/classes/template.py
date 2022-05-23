from detailedDesign.classes.Component import Component


class template(Component):
    def __init__(self, config):
        # Please pass my_config to any sub components as the second arg
        my_config = super().__init__(config)
