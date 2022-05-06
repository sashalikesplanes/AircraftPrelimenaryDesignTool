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

        params["balloonLift"] = lift

        radius = (
            volume / (np.pi * (4 / 3 + params['balloonLengthWidthRatio']))) ** (1 / 3)
        # print(liftToCarry, radius, volume)
        params["balloonVolume"] = volume
        params['balloonArea'] = np.pi * radius ** 2

        # Calculate mass of the balloon using plain pressure vessel
        pHydrogen = pHydrogenSeaLevel * params["compressionRatio"]
        dp = abs(pHydrogen - pAir)
        params["balloonStructuralMass"] = 2 * np.pi * radius ** 3 * \
            (1 + params['balloonLengthWidthRatio']) * \
            dp * rho_mat / sigma_mat * 0.25

    elif params["designConcept"] == 4:
        pass
