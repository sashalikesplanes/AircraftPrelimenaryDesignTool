from cgi import test
import numpy as np


from misc.constants import g


def wingSizing(params, rho):

    if ["designConcept"]:
        pass
    wingLift = params["totalMass"] * g - params["balloonLift"]
    params["wingArea"] = wingLift * params["liftFactor"] / (0.5 * rho * params["velocity"]
                                                            ** 2 * params["wingC_L_design"])
    # set wing area to zero in case of negative surface area
    if params["wingArea"] < 0:
        raise ValueError("wing area is negative")

    params["wingC_D"] = params['wingDragCorrection'] * params["wingC_D_0"]

    span = (params["wingArea"] * params["wingAspectRatio"]) ** 0.5
    chord = params["wingArea"] / span
    c2 = params["wingHalfChordSweep"]

    params["wingStructuralMass"] = 0.00125 * wingLift * \
        (span/np.cos(c2)) ** 0.75 * (1 + (6.3 * np.cos(c2) / span) ** 0.5) * (params["maxLoadFactor"] * 1.5) ** 0.55 * (
        span * params["wingArea"] / (params["thicknessOverChord"] * chord * wingLift * np.cos(c2))) ** 0.3


if __name__ == "__main__":
    testDict = {
        "totalMass": 10000,
        "liftRatio": 0.5,
        "wingC_L_design": 0.6,
        "liftFactor": 1.1,
        "wingDragCorrection": 1.1,
        "wingC_D_0": 0.05,
        "velocity": 140,
    }
    wingSizing(testDict, 1.225)
    print(testDict)
