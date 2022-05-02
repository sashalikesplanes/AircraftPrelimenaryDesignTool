import numpy as np

from preliminaryDesign.balloonSizing import balloonSizing
from preliminaryDesign.dragModel import dragModel
from preliminaryDesign.energyRequired import energyRequired
from preliminaryDesign.fuelMassEstimation import fuelMassEstimation
from preliminaryDesign.fuselageSizing import fuselageSizing
from preliminaryDesign.propulsionSizing import propulsionSizing
from preliminaryDesign.totalMassEstimation import totalMassEstimation
from preliminaryDesign.wingSizing import wingSizing

from misc.ISA import getDensity, getPressure

    fuselageSizing(parameters, dp)

def preliminaryDesign(parameters):
    """Perform preliminary design using design parameters"""

    # Get the density at the cruise altitude
    rho = getDensity(parameters["altitude"])
    dp = abs(getPressure(1000) - getPressure(parameters["altitude"]))

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
