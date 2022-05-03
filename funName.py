import numpy as np

from misc.ISA import getDensity, getPressure
from misc.constants import g
from conceptualDesign.fuselageSizing import fuselageSizing


if __name__ == "__main__":
    # Thingies
    v = 50  # [m/s]
    params = {}
    C_D = 0.055
    C_L = 0.6

    # Masses of things
    params["passengerMass"] = 100  # [kg]
    m_cabin = 30000  # [kg]
    n_pax = 500  # [-]
    params["cargoMass"] = 0  # [kg]

    # Dimensions of balloon
    l = 300  # [m]
    r = 20  # [m]
    h = 3000  # [m]
    compressionRatio = 5  # [-]

    # Lift from presence of fuel container
    rho_h2 = 0.08375  # [kg/m^3]
    rho_air = getDensity(h)  # [kg/m^3]
    V = l * np.pi * r ** 2  # [m^3]
    L_balloon = V * g * (rho_air - rho_h2 * compressionRatio)  # [N]
    dp = compressionRatio * 1e6 - getPressure(h)
    rho_mat = 2710
    sigma_mat = 276e6
    m_container = 2 * np.pi * r ** 3 * (1 + l / r) * dp * rho_mat / sigma_mat * 0.25

    # Lift required
    m_pax = n_pax * 100
    m_total = m_pax + m_cabin + m_container
    L_req = m_total * g
    L_wings = L_req - L_balloon
    print(f"Fraction of lift from wings: {L_wings/L_req}")
    S_w = L_wings / (0.5 * rho_air * v ** 2 * C_D)

    # Energy
    E_specific_h2 = 33.6e3 * 3600  # [J/kg]
    m_h2 = rho_h2 * compressionRatio * V  # [kg]
    E_h2 = m_h2 * E_specific_h2

    # Fuselage stuff
    if h > 3000:
        dp = getPressure(3000) - getPressure(h)
    else:
        dp = 0
    params["passengers"] = n_pax
    fuselageSizing(params, dp)

    # Drag of things
    balloonDrag = 0.5 * rho_air * v ** 2 * (np.pi * r ** 2 * 0.05)  # [N]
    fuselageDrag = 0.5 * rho_air * v ** 2 * (params['fuselageArea'] * 0.295)  # [N]
    wingDrag = 0.5 * rho_air * v ** 2 * (S_w * C_D)
    Drag = balloonDrag + fuselageDrag + wingDrag
    P_req = Drag * v

    # Endurance and range calculations
    endurance = E_h2 / P_req
    dist = endurance * v
    print(f"The endurance is {endurance} s")
    print(f"The range is {dist/1000} km")
