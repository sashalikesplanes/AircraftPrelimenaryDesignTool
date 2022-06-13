from misc.constants import R_air, g
import numpy as np

p0 = 101325
rho0 = 1.225
T0 = 273.15 + 15
a = -0.0065
gamma_air = 1.4


def getTemperature(h):
    """Calculates low level density using a provided height value"""
    # raise an error if the provided altitude is outside the accepted range
    if h > 11000 or h < 0:
        raise ValueError("Specified height not within acceptable range")

    # Calculate the temperature at the specified height
    T1 = T0 + a * h
    return T1


def getSpeedOfSound(h):
    """Calculate the speed of sounds at the given altitude"""
    temperature = getTemperature(h)

    return np.sqrt(gamma_air * R_air * temperature)


def getPressure(h):
    """Calculates low level density using a provided height value"""
    # raise an error if the provided altitude is outside the accepted range
    if h > 20000 or h < 0:
        raise ValueError("Specified height not within acceptable range")
    if h <= 11000:
        # Calculate the temperature at the specified height
        T1 = T0 + a * h

        # Calculate the density at the specified height
        p1 = p0 * (T1/T0) ** -(g / (a * R_air))
    if 11000 < h <= 20000:
        p1 = 22632 * np.e**(-g*(h-11000)/(R_air*216.65)) # numbers come from h =11000, start of tropopause
    return p1  # [N/m^2]


def getDensity(h):
    """Calculates low level density using a provided height value"""
    # raise an error if the provided altitude is outside the accepted range
    if h > 20000 or h < 0:
        raise ValueError("Specified height not within acceptable range")
    if h <= 11000:
        # Calculate the temperature at the specified height
        T1 = T0 + a * h

        # Calculate the density at the specified height
        rho1 = rho0 * (T1/T0) ** -((g/(a*R_air))+1)
    if 11000 < h <= 20000:
        p1 = getPressure(h)
        T1 = T0 + a * 11000
        rho1 = p1/(R_air*T1)
    return rho1  # [kg/m^3]


def getTemperature(h):
    if h > 20000 or h < 0:
        raise ValueError("Specified height not within acceptable range")
    if h <= 11000:
        # Calculate the temperature at the specified height
        T1 = T0 + a * h
    if 11000 < h <= 20000:
        T1 = T0 + a * 11000
    return T1
