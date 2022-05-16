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

    rootChord = 2 * params["wingArea"] / \
        (span * (1 + params["wingTaperRatio"]))
    MAC = 2 / 3 * rootChord * (1 + params["wingTaperRatio"] +
                               params["wingTaperRatio"] ** 2)/(1 + params["wingTaperRatio"])
    params["meanAerodynamicChord"] = MAC
    params["wingSpan"] = span

    flap_area_to_wing_area = params["flapAreaToWingArea"]
    flap_area = params["wingArea"] * flap_area_to_wing_area

    params["wingStructuralMass"] = 0.0051 * params["wingArea"] ** 0.649 * (flap_area) ** 0.1 * (params["ultimateLoadFactor"] * params["totalMass"] * g) ** 0.557 * (
        1 + params["wingTaperRatio"]) ** 0.1 * params["wingAspectRatio"] ** 0.5 / (params["thicknessOverChord"] ** 0.4 * np.cos(params["wingQuarterChordSweep"]))

    params["wingStructuralMass"] = params["wingStructuralMass"] * \
        params["wingStructureContingency"]
