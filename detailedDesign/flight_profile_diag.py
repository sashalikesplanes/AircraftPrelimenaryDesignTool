import numpy as np
from pathlib import Path
from dataclasses import dataclass, field
import matplotlib.pyplot as plt


takeoff_distance = 10 # km
cruise_altitude = 3 # km
avg_angle_of_climb = 8.8 # deg
cruise_range = 8000 # km 
taxi_range = 0.5 # km
climb_range = cruise_altitude / np.tan(avg_angle_of_climb / 180 * np.pi)


@dataclass
class ProfilePoint:
    name: str
    own_range: float # km
    previous_range: float
    altitude: float # km
    label_point: list[float] = field(default_factory=list)

    def setup_label_point(self, position='left'):
        if position == 'left':
            self.label_point = [self.previous_range + self.own_range - 1.0, self.altitude + 0.1]
        else:
            self.label_point = [self.previous_range + self.own_range + 0.1, self.altitude + 0.1]


@dataclass
class ProfilePoints:
    points: list[ProfilePoint] = field(default_factory=list)
    total_range: float = 0

    def add_point(self, name, range_, altitude):
        new_point = ProfilePoint(name, range_, self.total_range, altitude)
        self.points.append(new_point)

        self.total_range += range_

        if self.total_range < 300:
            self.points[-1].setup_label_point('left')
        else:
            self.points[-1].setup_label_point('right')

    @property
    def ranges(self):
        return [point.own_range + point.previous_range for point in self.points]

    @property
    def altitudes(self):
        return [point.altitude for point in self.points]

    @property
    def label_positions(self):
        return [point.label_point for point in self.points]

    @property
    def names(self):
        return [point.name for point in self.points]


points = ProfilePoints()
points.add_point('Taxi', taxi_range, 0)
points.add_point('Engine Start', 0, 0)
points.add_point('Takeoff', 10, 0)
points.add_point('Climb to Cruise', climb_range, cruise_altitude)
points.add_point('End of Cruise', cruise_range, cruise_altitude)
points.add_point('Descent and Land', climb_range, 0)
points.add_point('Taxi', taxi_range, 0)


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(points.ranges, points.altitudes, color='k')
ax2.plot(points.ranges, points.altitudes, color='k')

# for point in points.points:
    # ax1.annotate(point.name, point.label_point)
    # ax2.annotate(point.name, point.label_point)

ax1.set_xlim(0, points.ranges[3] + 5)
ax2.set_xlim(points.ranges[4] - 2, points.ranges[-1] + 1)

ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)

ax2.set_yticks([])

d = 0.015
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
# Bottom right line
ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
# Top right
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)

kwargs.update(transform=ax2.transAxes)
# Top left
ax2.plot((-d, +d), (-d, +d), **kwargs)
# Bottom Left
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)

fig.subplots_adjust(wspace=0.05)

fig.supxlabel('Range [km]')
ax1.set_ylabel('Altitude [km]')

plt.savefig(Path('plots', 'flightProfileDiagram.pdf'))
plt.close()
