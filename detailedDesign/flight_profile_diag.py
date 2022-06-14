import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt


takeoff_distance = 10 # km
cruise_altitude = 3 # km
avg_angle_of_climb = 8.8 # deg
cruise_range = 800 # km 
taxi_range = 0.5 # km

@dataclass
class ProfilePoint:
    name: str
    range_: int # km
    altitude: int # km

climb_range = cruise_altitude / np.tan(avg_angle_of_climb / 180 * np.pi)
        # range km, altitude m
points = [ProfilePoint('Taxi', taxi_range, 0),
          ProfilePoint('Engine Start', 0, 0),
          ProfilePoint('Takeoff', 10, 0),
          ProfilePoint('Climb to Cruise', climb_range, cruise_altitude),
          ProfilePoint('End of Cruise', cruise_range, cruise_altitude),
          ProfilePoint('Descent and Land', climb_range, 0),
          ProfilePoint('Taxi', taxi_range, 0)]
          
ranges = np.array([point.range_ for point in points]).cumsum()
altitudes = np.array([point.altitude for point in points])

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

ax1.plot(ranges, altitudes, color='green')
ax2.plot(ranges, altitudes, color='green')

ax1.set_xlim(0, ranges[3] + 5)
ax2.set_xlim(ranges[4] - 5, ranges[-1] + 1)

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


plt.show()

