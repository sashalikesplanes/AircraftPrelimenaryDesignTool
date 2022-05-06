import numpy as np

from conceptualDesign.payloadMassEstimation import payloadMassEstimation
from conceptualDesign.fuselageSizing import fuselageSizing, fuselageWeight
from conceptualDesign.totalMassEstimation import totalMassEstimation
from misc.ISA import getPressure


def initializeParameters(params):
    """Initialize all the things which should not be done within the main loop"""
    fuselageSizing(params)
    totalMassEstimation(params)
    fuselageWeight(params)
    payloadMassEstimation(params)  # Done

    # Crash for unacceptable values
    if params["wingTaperRatio"] > 1 or params["wingTaperRatio"] <= 1:
        raise ValueError("Taper ratio should be 1 at most")

    params["propEfficiency"] = params["engineEfficiency"] * \
        params["fuelCellEfficiency"]

    Lambda = params["wingTaperRatio"]
    c4 = params["wingQuarterChordSweep"]
    AR = params["wingAspectRatio"]
    params["wingHalfChordSweep"] = np.arctan(
        np.tan(c4) - 4/AR*((50-25)/100) * (1 - Lambda)/(1 + Lambda))

    if params["designConcept"] == 4:
        params["balloonArea"] = 0
        params["compressionRatio"] = 74/0.0083
