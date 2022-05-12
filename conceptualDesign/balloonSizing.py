import numpy as np
from misc.constants import g

rhoHydrogenGas = 0.08375  # kg/m^3
rhoHydrogenLiquid = 71  # kg/m^3
# aluminium 6061
rho_mat = 2710
rho_mat = 1550  # kg carbon fiber
sigma_mat = 241e6
sigma_mat = 1900e6  # Carbon Fiber source NASA
pHydrogenSeaLevel = 101325  # [Pa]
hydrogenMolarMass = 2.016e-3  # kg
R = 8.3145  # Universal gas constant


def balloonSizing(params, rhoAir, pAir, tAir):
    """
    Size the fuel tank / lifting balloon
    """

    # liftToCarry = params['totalMass'] * g * params["liftRatio"]
    # print(liftToCarry)
    #  = liftToCarry / \
    #          ((rhoAir - rhoHydrogen * params["compressionRatio"]) * g)

    if params["designConcept"] == 1:
        # Do balloon sizing for a blimp
        pass

    elif params["designConcept"] == 2 or params["designConcept"] == 3:

        totalHydrogenMass = params["fuelMass"] * \
            params["compressionRatio"] / (params["compressionRatio"] - 1)

        params["liftingHydrogenMass"] = totalHydrogenMass - params["fuelMass"]
        volume = totalHydrogenMass / \
            (rhoHydrogenGas * params["compressionRatio"])
        lift = volume * g * (rhoAir)
        radius = (volume / (4 / 3 * np.pi *
                  params['balloonFinesseRatio'])) ** (1/3)

        params["balloonArea"] = np.pi * radius ** 2
        if lift < 0:
            lift = 0
        params["balloonLift"] = lift
        params["balloonVolume"] = volume
        params["balloonRadius"] = radius
        if params["balloonArea"] == 0:
            params["balloonLength"] = 0
        else:
            params["balloonLength"] = radius * \
                params['balloonFinesseRatio'] * 2

        # Calculate mass of the balloon using plain pressure vessel
        pHydrogen = pHydrogenSeaLevel * params["compressionRatio"]
        p = totalHydrogenMass / hydrogenMolarMass * R * tAir / volume
        params["balloonPressure"] = p
        dp = abs(p - pAir)

        ratio = dp / (2 * sigma_mat / params["factorOfSafety"] + dp)
        wallThickness = ratio * (2 * radius)
        params["wallThickness"] = wallThickness
        eccentricity = (1 - (1 / params['balloonFinesseRatio']) ** 2)
        balloonSurfaceArea = 2 * np.pi * radius ** 2 * \
            (1 + params['balloonFinesseRatio'] /
             eccentricity * np.arcsin(eccentricity))
        params["balloonStructuralMass"] = balloonSurfaceArea * \
            wallThickness * rho_mat * 0.5 * params["balloonMassContingency"]
        params["balloonSurfaceArea"] = balloonSurfaceArea

    elif params["designConcept"] == 4:
        m_fuel = params["fuelMass"]
        # p = 101325
        # T = 20
        # n = m_fuel * 1000 / (2 * 1.008)  # moles
        # print(f"{n} Moles")
        # V_h2 = n*R_h2*T/p
        V_h2 = m_fuel / rhoHydrogenLiquid  # m^3
        r = 1.25  # m  (radius of fuel tank)
        # print(f"{V_h2} m^3")
        params["balloonLength"] = (V_h2)/(np.pi*r**2)
        # print(f"Balloon length: {params['balloonLength']} m")

        params["balloonStructuralMass"] = m_fuel * \
            params["containerToFuelMassRatio"]
