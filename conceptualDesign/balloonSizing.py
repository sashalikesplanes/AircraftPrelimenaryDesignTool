import numpy as np

g = 9.80665
rhoHydrogen = 0.08375  # kg/m^3
# aluminium 6061
rho_mat = 2710
sigma_mat = 241e6
pHydrogenSeaLevel = 101325  # [Pa]


# test comment


def balloonSizing(params, rhoAir, pAir):
    # liftToCarry = params['totalMass'] * g * params["liftRatio"]
    # print(liftToCarry)
    #  = liftToCarry / \
    #          ((rhoAir - rhoHydrogen * params["compressionRatio"]) * g)

    totalHydrogenMass = params["fuelMass"] * \
        params["compressionRatio"] / (params["compressionRatio"] - 1)

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


if __name__ == "__main__":
    testDict = {
        "totalMass": 10000,
        "liftRatio": 0.5,
        "compressionRatio": 1.2,
    }
    balloonSizing(testDict, 1.225)
    print(testDict)
