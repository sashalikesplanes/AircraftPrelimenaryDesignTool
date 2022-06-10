import numpy as np

from misc.ISA import getPressure


def calculate_stress(x, y, z, t, aircraft):
    # Base the radius on the y and z coordinates of the point
    r = (y ** 2 + z ** 2) ** 0.5

    S_y = -aircraft.FuselageGroup.Tail.VerticalTail.F_w
    S_z = aircraft.FuselageGroup.Fuselage.longitudinal_shear[x]
    M_z = (aircraft.FuselageGroup.Fuselage.Cabin.length - aircraft.FuselageGroup.Aircraft.get_cg()[0]) * S_y
    M_y = aircraft.FuselageGroup.Fuselage.longitudinal_moment[x]
    T = S_y * (aircraft.FuselageGroup.Tail.VerticalTail.span / 2)

    # first moment of area
    a = aircraft.FuselageGroup.Fuselage.outer_height
    b = aircraft.FuselageGroup.Fuselage.outer_width

    Q_z = 4 * b ** 2 * a / 3 - (4 * (b - 2 * t) ** 2 * (a - 2 * t) / 3)
    Q_y = 4 * a ** 2 * b / 3 - (4 * (a - 2 * t) ** 2 * (b - 2 * t) / 3)

    I_yy = np.pi / 64 * (a ** 3 * b - (a - 2 * t) ** 3 * (b - 2 * t))
    I_zz = np.pi / 64 * (b ** 3 * a - (b - 2 * t) ** 3 * (a - 2 * t))
    delta_P = np.abs(getPressure(aircraft.FuselageGroup.Aircraft.states['cruise'].altitude) - getPressure(
        aircraft.FuselageGroup.Fuselage.Cabin.cabin_pressure_altitude))
    J_0 = I_yy + I_zz

    # Calculate stresses
    sigma_x = M_z * y / I_zz + M_y * z / I_yy + delta_P * r / t
    sigma_y = 2 * r * delta_P / t

    shear = -(S_y * Q_z) / (I_zz * t) - (S_z * Q_y) / (I_yy * t) + T * r / J_0

    tau_max = (((sigma_x - sigma_y) / 2)**2 + shear ** 2) ** 0.5

    sigma_1 = (sigma_x + sigma_y) / 2 + tau_max
    sigma_2 = (sigma_x + sigma_y) / 2 - tau_max
    result = (sigma_x, sigma_y)
    # print(result, shear)
    return result
