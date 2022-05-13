import numpy as np
from misc.constants import g, rho_h2, R
from misc.ISA import getPressure, getTemperature


hydrogenMolarMass = 2.016e-3  # [kg/mole]

# aluminium 6061
rho_mat = 2710
sigma_mat = 241 * 10 ** 6


def fuselageSizing(params):
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
        n_aisles = 3
        k_cabin = 1.25

    l_cabin = n_rows * k_cabin
    # print(f"Cabin length: {l_cabin}")
    w_aisle = 0.6
    w_seat = 0.44
    w_armrest = 0.05

    w_fuselage = n_aisles * w_aisle + w_armrest * (n_sa+n_aisles+1) + n_sa * w_seat
    # End of ADSEE I

    d_inner = w_fuselage
    # print(f"Inner fuselage diameter: {d_inner}")
    d_outer = 1.045 * d_inner + 0.084
    # print(f"Outer fuselage diameter: {d_outer}")

    # Assume that the weight of the mass is 10% that of a cylinder with the thickness of the fuselage
    m_fuselage = np.pi * ((d_outer/2) ** 2 - (d_inner/2)
                          ** 2) * l_cabin * rho_mat * 0.1
    # print(f"{m_fuselage} kg")

    # https://en.wikipedia.org/wiki/Pressure_vessel
    # shape is a stadium of revolution
    # m_cabin = 2 * np.pi * r_fuselage ** 2 * (l_cabin - r_fuselage) * dp * rho_mat / sigma_mat * params["safetyFactor"]
    # print(m_cabin)
    # print(r_fuselage, l_cabin)
    # https://www.researchgate.net/publication/264864827_Analytical_Weight_Estimation_Method_for_Oval_Fuselages_in_Conventional_and_Novel_Aircraft

    # m_cabin = 44.4e3
    params["cabinLength"] = l_cabin
    params["fuselageStructuralMass"] = m_fuselage
    params["fuselageArea"] = np.pi * (d_outer / 2) ** 2
    params["fuselageDiameter"] = d_outer
    params["fuselageInnerDiameter"] = d_inner


def fuselageWeight(params):
    """Estimate the weight of the fuselage"""
    # /!\ RETARD UNITS /!\
    # Extract all relevant variables from params and convert them to retard units
    Wto = params["totalMass"] * 2.20462  # [lbs]
    lfus = params["cabinLength"] / 0.3048  # [ft]
    rfus = (params["fuselageDiameter"] / 2) / 0.3048  # [ft]
    c4 = params["wingQuarterChordSweep"]  # [rad]
    AR = params["wingAspectRatio"]  # [-]
    Sref = params["wingArea"] / 10.7639  # [ft^2]
    labda = params["wingTaperRatio"]  # [-]

    Nult = 2.5 * 1.65  # [-]
    Sfuswet = 2 * np.pi * lfus * rfus + 4 * np.pi * rfus ** 2  # [ft^2]
    KWS = 0.75 * ((1+2*labda)/(1+labda)*(AR*Sref)**2*np.tan(c4))/lfus  # [?]

    # This can be used while unit testing in order to check kws
    if 'kws' in params:
        params['kws'] = KWS

    # Calculate the fuselage weight using the sketchy method
    Wfus = 0.4886 * (Wto * Nult) ** 0.5 * lfus ** 0.25 * \
        Sfuswet ** 0.302 * (1 + KWS) ** 0.4
    params["fuselageStructuralMass"] = Wfus / 2.20462

    r_tank = (params["fuselageInnerDiameter"] / 2)
    A_tank = np.pi * r_tank ** 2
    CR = params["compressionRatio"]

    fuelMass = params["fuelMass"]

    V_req = fuelMass / (rho_h2 * CR)
    l_tank = V_req / A_tank
    # print("Hello world!")
    # print(fuelMass)
    # print(V_req)
    # print(l_tank)

    # Save container parameters
    params["balloonVolume"] = V_req
    params["balloonRadius"] = r_tank
    params["balloonLength"] = l_tank

    # Save total fuselage length
    l_cockpit = 4  # [m]
    tail_finesse = 3  # [-] between 3 and 6 for flying boats
    params["fuselageLength"] = l_tank + params["cabinLength"] + l_cockpit + params["fuselageDiameter"] * tail_finesse

    h = params["altitude"]
    pAir = getPressure(h)
    tAir = getTemperature(h)

    # Calculate mass of the balloon using plain pressure vessel
    p = fuelMass / hydrogenMolarMass * R * tAir / V_req
    params["balloonPressure"] = p
    dp = abs(p - pAir)

    ratio = dp / (2 * sigma_mat / params["factorOfSafety"] + dp)
    wallThickness = ratio * (2 * r_tank)
    params["wallThickness"] = wallThickness
    balloonSurfaceArea = np.pi * r_tank ** 2 + 2 * np.pi * r_tank * l_tank
    balloonMass = balloonSurfaceArea * wallThickness * rho_mat * 0.5 * params["balloonMassContingency"]
    params["balloonStructuralMass"] = balloonMass
