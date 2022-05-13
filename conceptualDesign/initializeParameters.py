import numpy as np

from conceptualDesign.payloadMassEstimation import payloadMassEstimation
from conceptualDesign.fuselageSizing import fuselageSizing, fuselageWeight
from conceptualDesign.totalMassEstimation import totalMassEstimation
from misc.ISA import getPressure


def initializeParameters(params):
    """Initialize all the things which should not be done within the main loop"""
    fuselageSizing(params)
    payloadMassEstimation(params)
    totalMassEstimation(params)
    fuselageWeight(params)
    # Done

    # Crash for unacceptable values
    if params["wingTaperRatio"] > 1 or params["wingTaperRatio"] <= 0:
        raise ValueError(
            f"Taper should be in the following range: 0 < λ <= 1, currently {params['wingTaperRatio']}")

    params["propEfficiency"] = params["engineEfficiency"] * \
        params["fuelCellEfficiency"]

    Lambda = params["wingTaperRatio"]
    c4 = params["wingQuarterChordSweep"]
    AR = params["wingAspectRatio"]
    span = np.sqrt(params["wingArea"] * AR)

    rootChord = 2 * params["wingArea"] / \
        (span * (1 + params["wingTaperRatio"]))
    MAC = 2 / 3 * rootChord * (1 + params["wingTaperRatio"] +
                               params["wingTaperRatio"] ** 2)/(1 + params["wingTaperRatio"])
    params["meanAerodynamicChord"] = MAC

    params["wingHalfChordSweep"] = np.arctan(
        np.tan(c4) - 4/AR*((50-25)/100) * (1 - Lambda)/(1 + Lambda))

    params["balloonArea"] = 0
