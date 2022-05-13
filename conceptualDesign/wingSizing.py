from cgi import test
import numpy as np


from misc.constants import g


def wingSizing(params, rho):

    wingLift = params["totalMass"] * g
    params["wingArea"] = wingLift * params["liftFactor"] / (0.5 * rho * params["velocity"]
                                                            ** 2 * params["wingC_L_design"])

    params["wingC_D"] = params['wingDragCorrection'] * params["wingC_D_0"]

    span = np.sqrt(params["wingArea"] * params["wingAspectRatio"])
    chord = span / params["wingAspectRatio"]
    c2 = params["wingHalfChordSweep"]

    rootChord = 2 * params["wingArea"] / (span * (1 + params["wingTaperRatio"]))
    MAC = 2 / 3 * rootChord * (1 + params["wingTaperRatio"] +
                               params["wingTaperRatio"] ** 2)/(1 + params["wingTaperRatio"])
    params["meanAerodynamicChord"] = MAC
    params["wingSpan"] = span

    params["wingStructuralMass"] = 0.00125 * wingLift * \
        (span/np.cos(c2)) ** 0.75 * (1 + (6.3 * np.cos(c2) / span) ** 0.5) * (params["maxLoadFactor"] * 1.5) ** 0.55 * (
        span * params["wingArea"] / (params["thicknessOverChord"] * chord * wingLift * np.cos(c2))) ** 0.3
