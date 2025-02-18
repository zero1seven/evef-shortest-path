from typing import NamedTuple

import math


METERS_IN_LIGHTYEAR = 9460730472580800

def convert_meters_to_light_years(meters: int) -> int:
	return meters/METERS_IN_LIGHTYEAR

def convert_light_years_to_meters(lightyears: int) -> int:
    return int(lightyears)*METERS_IN_LIGHTYEAR

#Calculates the center of a solar systems distance in METERS
def distance(sourcesystem: tuple, sourcedest: tuple) -> int:
    # Implement the logic to calculate the distance between two gates
    # Calculate absolute differences
    dx = abs(sourcesystem[0] - sourcedest[0])
    dy = abs(sourcesystem[1] - sourcedest[1])
    dz = abs(sourcesystem[2] - sourcedest[2])

    # Sum of squares (distance squared in meters)
    distanceMeters = math.sqrt((dx * dx) + (dy * dy) + (dz * dz))
    return distanceMeters
