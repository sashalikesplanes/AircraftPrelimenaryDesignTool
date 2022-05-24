from pathlib import Path
from misc.openData import openData
from misc.ISA import getPressure, getDensity, getTemperature, getSpeedOfSound


class State:
    def __init__(self, name):
        self.name = name

        source = openData(Path('data', 'states', f'{name}.yaml'))
        for key in source:
            print(key, source[key])

        self.velocity = source["velocity"]
        self.altitude = source["altitude"]
        self.range = source["range"]
        h = self.altitude

        self.pressure = getPressure(h)
        self.density = getDensity(h)
        self.temperature = getTemperature(h)
        self.speed_of_sound = getSpeedOfSound(h)
