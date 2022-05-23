import yaml


def openData(filename):
    """Open data file with design parameters"""
    with open(filename) as file:
        result = yaml.load(file, Loader=yaml.FullLoader)

    return result
