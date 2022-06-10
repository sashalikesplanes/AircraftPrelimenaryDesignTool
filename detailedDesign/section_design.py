import numpy as np


C = 4
E_carbon = 70e9
E_aluminum = 71.7e9
v = 1/3

n_stringers = 6


def stringer_crippling():
    pass
    # sigma_cc_over_sigma_y = alpha * (C / sigma_y * np.pi ** 2 * E / (12 * (1-v**2)) * (t / b) ** 2) ** (1 - n)


def plate_crippling(t, aircraft):
    circumference = (aircraft.FuselageGroup.Fuselage.outer_height + aircraft.FuselageGroup.Fuselage.outer_width) / 2 * np.pi

    b = circumference / n_stringers
    sigma_cc = 445.6e9  # [Pa] Crippling of stringers
    area_stiffner = 260e-6  # [m^2]

    sigma_cr = C * np.pi ** 2 * E_carbon / (12 * (1 - v ** 2)) * (t/b) ** 2  # [Pa] Crippling of plates

    sigma_cc_panel = (sigma_cc * area_stiffner + sigma_cr * t * b) / (t * b + area_stiffner)
    print(sigma_cc_panel * 10 ** -6, "[MPa]")
