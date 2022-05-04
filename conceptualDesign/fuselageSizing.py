import numpy as np
from misc.constants import g


# aluminium 6061
rho_mat = 2710
sigma_mat = 241 * 10 ** 6


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

    w_fuselage = n_aisles * w_aisle + w_armrest * (n_sa+n_aisles+1) + n_sa * w_seat
    # End of ADSEE I

    # Total mass of payload
    m_total = m_cargo + m_pax

    d_inner = w_fuselage
    # print(f"Inner fuselage diameter: {d_inner}")
    d_outer = 1.045 * d_inner + 0.084
    # print(f"Outer fuselage diameter: {d_outer}")

    # Assume that the weight of the mass is 10% that of a cylinder with the thickness of the fuselage
    m_fuselage = (np.pi * (d_outer/2) ** 2 - np.pi * (d_inner/2) ** 2) * l_cabin * rho_mat * 0.1
    # print(f"{m_fuselage} kg")

    # https://en.wikipedia.org/wiki/Pressure_vessel
    # shape is a stadium of revolution
    # m_cabin = 2 * np.pi * r_fuselage ** 2 * (l_cabin - r_fuselage) * dp * rho_mat / sigma_mat * params["safetyFactor"]
    # print(m_cabin)
    # print(r_fuselage, l_cabin)
    # https://www.researchgate.net/publication/264864827_Analytical_Weight_Estimation_Method_for_Oval_Fuselages_in_Conventional_and_Novel_Aircraft

    # m_cabin = 44.4e3
    params["cabinLength"] = l_cabin
    m_cabin = m_fuselage
    params["fuselageStructuralMass"] = m_cabin
    params["fuselageArea"] = np.pi * (d_outer / 2) ** 2
    params["fuselageDiameter"] = d_outer


def fuselageWeight(params):
    Wto = params["totalMass"] * 2.20462
    Nult = 2.5 * 1.65
    lfus = params["cabinLength"] * 0.3048
    rfus = (params["fuselageDiameter"] / 2) * 0.3048
    Sfuswet = 2 * np.pi * lfus + np.pi * rfus ** 2

    c4 = 0
    AR = params["wingAspectRatio"]
    Sref = params["wingArea"] / 10.7639
    labda = 1
    KWS = 0.75 * ((1+2*labda)/(1+labda)*(AR*Sref)**2*np.tan(c4))/lfus

    Wfus = 0.4886 * (Wto * Nult) ** 0.5 * lfus ** 0.25 * Sfuswet ** 0.302 * (1 + KWS) ** 0.4
    params["fuselageStructuralMass"] = Wfus / 2.20462
