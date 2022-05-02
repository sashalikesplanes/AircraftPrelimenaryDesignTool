import numpy as np


bullShitFactor = 3


def fuselageSizing(params, dp):
    print(f"Pressure difference: {dp}")
    n_pax = params["passengers"]
    m_cargo = params["cargoMass"]
    m_pax = n_pax * params["passengerMass"]

    # Total mass of payload
    m_total = m_cargo + m_pax

    r = params["fuselageRadius"]
    l = params["fuselageLength"]

    # aluminium 6061
    rho_mat = 2710
    sigma_mat = 241 * 10 ** 6

    # https://en.wikipedia.org/wiki/Pressure_vessel
    # shape is a stadium of revolution
    m_cabin = 2 * np.pi * r ** 2 * \
        (l - r) * dp * rho_mat / sigma_mat * params["safetyFactor"]
    print(m_cabin)

    params["fuselageArea"] = np.pi * r ** 2
