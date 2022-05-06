import numpy as np

g = 9.80665
rhoHydrogen = 0.08375  # kg/m^3
# aluminium 6061
rho_mat = 2710
sigma_mat = 241e6
pHydrogenSeaLevel = 101325  # [Pa]


def balloonSizing(params, rhoAir, pAir):
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
        volume = totalHydrogenMass / (rhoHydrogen * params["compressionRatio"])
        lift = volume * g * (rhoAir - rhoHydrogen * params["compressionRatio"])
        radius = (volume / (4 / 3 * np.pi *
                  params['balloonFinesseRatio'])) ** (1/3)

        params["balloonLift"] = lift
        params["balloonVolume"] = volume
        params["balloonRadius"] = radius
        params["balloonArea"] = np.pi * radius ** 2
        params["balloonLength"] = radius * params['balloonFinesseRatio'] * 2

        # Calculate mass of the balloon using plain pressure vessel
        pHydrogen = pHydrogenSeaLevel * params["compressionRatio"]
        dp = abs(pHydrogen - pAir)
        wallThickness = dp * radius * \
            params["factorOfSafety"] / (2 * sigma_mat)
        eccentricity = (1 - (1 / params['balloonFinesseRatio']) ** 2)
        balloonSurfaceArea = 2 * np.pi * radius ** 2 * \
            (1 + params['balloonFinesseRatio'] /
             eccentricity * np.arcsin(eccentricity))
        params["balloonStructuralMass"] = balloonSurfaceArea * \
            wallThickness * rho_mat

    elif params["designConcept"] == 4:
        pass
