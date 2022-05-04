g = 9.80665


def wingSizing(params, rho):
    # Make the wing big enough to lift everything not carried by the balloon
    wingLift = params["totalMass"] * g - params["balloonLift"]
    params["wingArea"] = wingLift * params["liftFactor"] / (0.5 * rho * params["velocity"]
                                                            ** 2 * params["wingC_L_design"])

    params["wingC_D"] = params['wingDragCorrection'] * params["wingC_D_0"]

    span = (params["wingArea"] * params["wingAspectRatio"]) ** 0.5
    chord = params["wingArea"] / span

    # Class 2 wing estimation method
    params["wingStructuralMass"] = 0.0017 * wingLift * \
        (span) ** 0.75 * (1 + (6.3 / span) ** 0.5) * (params["maxLoadFactor"] * 1.5) ** 0.55 * (
            span * params["wingArea"] / (params["thicknessOverChord"] * chord * wingLift)) ** 0.3
