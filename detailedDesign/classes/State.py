from pathlib import Path

from misc.openData import openData


class State:
    def __init__(self, name):
        self.name = name

        source = openData(Path('data', 'states', f'{name}.yaml'))
        for key in source:
            print(key, source[key])

        self.velocity = source["velocity"]
        self.altitude = source["altitude"]
