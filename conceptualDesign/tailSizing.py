import numpy as np


def tailSizing(params):

    vertical_tail_volume_coefficient = 0.09
    horizontal_tail_volume_coefficient = 1.0

    # of fuselage length, an initial estimate before wing is positioned
    tail_arm_fraction = 0.5
    tail_arm = tail_arm_fraction * params["fuselageLength"]

    vertical_tail_area = vertical_tail_volume_coefficient * \
        params["wingSpan"] * params["wingArea"] / tail_arm
    horizontal_tail_area = horizontal_tail_volume_coefficient * \
        params["meanAerodynamicChord"] * params["wingArea"] / tail_arm

    params["tailStructuralMass"] = 0.051 * params["diveSpeed"] * \
        (vertical_tail_area + horizontal_tail_area) ** 1.2 / \
        np.sqrt(np.cos(params["wingQuarterChordSweep"])
                ) * params["tailStructuralContingency"]
