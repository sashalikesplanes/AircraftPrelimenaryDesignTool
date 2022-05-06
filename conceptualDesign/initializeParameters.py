import numpy as np

from conceptualDesign.payloadMassEstimation import payloadMassEstimation
from conceptualDesign.fuselageSizing import fuselageSizing, fuselageWeight
from misc.ISA import getPressure


def initializeParameters(params):
    # Initialize shit that should be
    dp = abs(getPressure(1000) - getPressure(params["altitude"]))
    if dp < 0:
        dp = 0
    fuselageSizing(params, dp)  # Done

    fuselageWeight(params)

    payloadMassEstimation(params)  # Done

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
