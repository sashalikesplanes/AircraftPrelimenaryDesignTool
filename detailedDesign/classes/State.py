from pathlib import Path
from misc.openData import openData
from misc.ISA import getPressure, getDensity, getTemperature, getSpeedOfSound


class State:
    def __init__(self, name):
        self.name = name

        self.source = openData(Path('data', 'states', f'{name}.yaml'))

    @property
    def velocity(self):
        return self.source["velocity"]

    @property
    def altitude(self):
        return self.source["altitude"]

    @property
    def range(self):
        return self.source["range"]

    @property
    def pressure(self):
        return getPressure(self.altitude)

    @property
    def density(self):
        return getDensity(self.altitude)

    @property
    def temperature(self):
        return getTemperature(self.altitude)

    @property
    def speed_of_sound(self):
        return getSpeedOfSound(self.altitude)
