from misc.constants import R_air, g

p0 = 101325
rho0 = 1.225
T0 = 273.15 + 15
a = -0.0065


def getDensity(h):
    """Calculates low level density using a provided height value"""
    # raise an error if the provided altitude is outside the accepted range
    if h > 11000 or h < 0:
        raise ValueError("Specified height not within acceptable range")

    # Calculate the temperature at the specified height
    T1 = T0 + a * h

    # Calculate the density at the specified height
    rho1 = rho0 * (T1/T0) ** -((g/(a*R_air))+1)
    return rho1  # [kg/m^3]


def getPressure(h):
    """Calculates low level density using a provided height value"""
    # raise an error if the provided altitude is outside the accepted range
    if h > 11000 or h < 0:
        raise ValueError("Specified height not within acceptable range")

    # Calculate the temperature at the specified height
    T1 = T0 + a * h

    # Calculate the density at the specified height
    p1 = p0 * (T1/T0) ** -(g / (a * R_air))
    return p1  # [N/m^2]
