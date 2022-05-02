from conceptualDesign.payloadMassEstimation import payloadMassEstimation
from conceptualDesign.fuselageSizing import fuselageSizing
from misc.ISA import getPressure


def initializeParameters(params):
    # Initialize shit that should be
    dp = abs(getPressure(1000) - getPressure(params["altitude"]))
    fuselageSizing(params, dp)  # Done

    payloadMassEstimation(params)  # Done

    params["propEfficiency"] = params["engineEfficiency"] * \
        params["fuelCellEfficiency"]
