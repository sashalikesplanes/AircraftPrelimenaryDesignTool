import numpy as np

g = 9.80665
rhoHydrogen = 0.08375  # kg/m^3


def balloonSizing(params, rhoAir):
    liftToCarry = params['totalMass'] * g * params["liftRatio"]
    print(liftToCarry)
    volume = liftToCarry / \
        ((rhoAir - rhoHydrogen * params["compressionRatio"]) * g)

    radius = (volume * 3 / 4 / np.pi)**(1/3)
    print(liftToCarry, radius, volume)
    params['balloonArea'] = np.pi * radius ** 2


if __name__ == "__main__":
    testDict = {
        "totalMass": 10000,
        "liftRatio": 0.5,
        "compressionRatio": 1.2,
    }
    balloonSizing(testDict, 1.225)
    print(testDict)
