import numpy as np
from dataclasses import dataclass

takeoff_distance = 10 # km
cruise_altitude = 3 # km

@dataclass
class ProfilePoint:
    name: str
    range_: int # km
    altitude: int # km

        # range km, altitude m
points = [ProfilePoint('Engine Start', 0, 0),
          ProfilePoint('Takeoff', 10, 0),
          ProfilePoint('Climb to Cruise', 


