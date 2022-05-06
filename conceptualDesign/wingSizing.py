from cgi import test
from nbformat import ValidationError
import numpy as np


from misc.constants import g


def wingSizing(params, rho):

    # Check if blimp concept has enough lift to compensate the weight and not too much
    if ["designConcept"] == 1:
        if abs(params["totalMass"] * g - params["balloonLift"]) > 5:
            raise ValidationError("Balloon Lift does not match weight")
        params["wingArea"] = 0
        params["wingStructuralMass"] = 0

    # Check for aircraft concept that no lift is calculated from the fuel
    elif ["designConcept"] == 4:
        if abs(params["balloonLift"]) > 5:
            raise ValidationError(
                "In a plane concept there is some balloon lift...")

    wingLift = params["totalMass"] * g - params["balloonLift"]
    params["wingArea"] = wingLift * params["liftFactor"] / (0.5 * rho * params["velocity"]
                                                            ** 2 * params["wingC_L_design"])
    # set wing area to zero in case of negative surface area
    if params["wingArea"] < 0:
        raise ValidationError("wing area is negative")

    params["wingC_D"] = params['wingDragCorrection'] * params["wingC_D_0"]

    span = (params["wingArea"] * params["wingAspectRatio"]) ** 0.5
    chord = params["wingArea"] / span
    c2 = params["wingHalfChordSweep"]

    params["wingStructuralMass"] = 0.00125 * wingLift * \
        (span/np.cos(c2)) ** 0.75 * (1 + (6.3 * np.cos(c2) / span) ** 0.5) * (params["maxLoadFactor"] * 1.5) ** 0.55 * (
        span * params["wingArea"] / (params["thicknessOverChord"] * chord * wingLift * np.cos(c2))) ** 0.3
