import numpy as np

from conceptualDesign.balloonSizing import balloonSizing
from conceptualDesign.dragModel import dragModel
from conceptualDesign.energyRequired import energyRequired
from conceptualDesign.fuelMassEstimation import fuelMassEstimation
from conceptualDesign.fuselageSizing import fuselageSizing
from conceptualDesign.propulsionSizing import propulsionSizing
from conceptualDesign.totalMassEstimation import totalMassEstimation
from conceptualDesign.wingSizing import wingSizing

from misc.ISA import getDensity, getPressure


def conceptualDesign(parameters):
    """Perform preliminary design using design parameters"""

    # Get the density at the cruise altitude
    rho = getDensity(parameters["altitude"])
    dp = abs(getPressure(1000) - getPressure(parameters["altitude"]))

    fuselageSizing(parameters, dp)

    # parameters["totalMass"] = parameters["fuselageMass"]

    i = 0
    while i < 10000:
        # wing
        wingSizing(parameters, rho)  # Done

        # balloon sizing
        balloonSizing(parameters, rho)  # Done

        # drag model
        dragModel(parameters, rho)  # Done

        # propulsion sizing
        propulsionSizing(parameters)

        # energy required
        energyRequired(parameters)

        # fuel mass estimation
        fuelMassEstimation(parameters)

        # total mass
        totalMassEstimation(parameters)

        # check if converged

        i += 1

    print("DONE :))))")
    return parameters
