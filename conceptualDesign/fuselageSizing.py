import numpy as np


bullShitFactor = 3


def fuselageSizing(params, dp):
    # print(f"Pressure difference: {dp}")
    n_pax = params["passengers"]
    m_cargo = params["cargoMass"]
    m_pax = n_pax * params["passengerMass"]

    # ADSEE I starts here
    n_sa = np.ceil(0.45 * n_pax ** 0.5)
    n_rows = np.ceil(n_pax/n_sa)
    if n_sa <= 6:
        n_aisles = 1
        k_cabin = 1.08
    elif n_sa <= 12:
        n_aisles = 2
        k_cabin = 1.17
    else:
        raise IOError

    l_cabin = n_rows * k_cabin
    # print(f"Cabin length: {l_cabin}")
    w_aisle = 0.6
    w_seat = 0.44
    w_armrest = 0.05

    w_fuselage = n_aisles * w_aisle + w_armrest * \
        (n_sa+n_aisles+1) + n_sa * w_seat
    # End of ADSEE I

    # Total mass of payload
    m_total = m_cargo + m_pax

    r_fuselage = (1.045 * w_fuselage + 0.084) / 2

    # aluminium 6061
    rho_mat = 2710
    sigma_mat = 241 * 10 ** 6

    # https://en.wikipedia.org/wiki/Pressure_vessel
    # shape is a stadium of revolution
    # m_cabin = 2 * np.pi * r_fuselage ** 2 * (l_cabin - r_fuselage) * dp * rho_mat / sigma_mat * params["safetyFactor"]
    # print(m_cabin)
    # print(r_fuselage, l_cabin)
    # https://www.researchgate.net/publication/264864827_Analytical_Weight_Estimation_Method_for_Oval_Fuselages_in_Conventional_and_Novel_Aircraft
    # m_cabin = 44.4e3
    # params["fuselageStructuralMass"] = m_cabin
    params["fuselageArea"] = np.pi * r_fuselage ** 2
