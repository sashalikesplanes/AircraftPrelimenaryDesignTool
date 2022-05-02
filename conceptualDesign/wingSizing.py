from cgi import test


g = 9.80665


def wingSizing(params, rho):
    wingLift = params["totalMass"] * g - params["balloonLift"]
    params["wingArea"] = wingLift * params["liftFactor"] / (0.5 * rho * params["velocity"]
                                                            ** 2 * params["wingC_L_design"])

    params["wingC_D"] = params['wingDragCorrection'] * params["wingC_D_0"]

    span = (params["wingArea"] * params["aspectRatio"]) ** 0.5
    chord = params["wingArea"] / span

    params["wingStructuralMass"] = 0.0017 * wingLift * \
        (span) ** 0.75 * (1 + (6.3 / span) ** 0.5) * (params["maxLoadFactor"] * 1.5) ** 0.55 * (
            span * params["wingArea"] / (params["thicknessOverChord"] * chord * wingLift)) ** 0.3


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
