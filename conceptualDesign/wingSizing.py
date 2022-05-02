from cgi import test


g = 9.80665


def wingSizing(params, rho):
    params["wingArea"] = params["totalMass"] * g * (1 - params["liftRatio"]) * \
        params["liftFactor"] / (0.5 * rho * params["velocity"]
                                ** 2 * params["wingC_L_design"])

    params["wingC_D"] = params['wingDragCorrection'] * params["wingC_D_0"]


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
