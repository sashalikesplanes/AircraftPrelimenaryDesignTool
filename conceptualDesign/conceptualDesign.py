import numpy as np

from conceptualDesign.balloonSizing import balloonSizing
from conceptualDesign.dragModel import dragModel
from conceptualDesign.energyRequired import energyRequired
from conceptualDesign.fuelMassEstimation import fuelMassEstimation
from conceptualDesign.fuselageSizing import fuselageSizing
from conceptualDesign.propulsionSizing import propulsionSizing
from conceptualDesign.totalMassEstimation import totalMassEstimation
from conceptualDesign.wingSizing import wingSizing
from conceptualDesign.payloadMassEstimation import payloadMassEstimation

from misc.ISA import getDensity, getPressure


def conceptualDesign(parameters):
    """Perform preliminary design using design parameters"""

    # Get the density at the cruise altitude
    rho = getDensity(parameters["altitude"])
    dp = abs(getPressure(1000) - getPressure(parameters["altitude"]))
    pAir = getPressure(parameters["altitude"])

    payloadMassEstimation(parameters)  # Done
    fuselageSizing(parameters, dp)  # Done

    totalMassEstimation(parameters)  # Done

    i = 0
    while i < 10000:
        # wing
        wingSizing(parameters, rho)  # Done

        # balloon sizing
        balloonSizing(parameters, rho, pAir)  # Done

        # drag model
        dragModel(parameters, rho)  # Done

        # propulsion sizing
        propulsionSizing(parameters)  # TODO need numbers for this

        # energy required
        energyRequired(parameters)  # Done

        # fuel mass estimation
        fuelMassEstimation(parameters)  # Done

        # total mass
        totalMassEstimation(parameters)  # DOne

        # check if converged

        i += 1

    print("DONE :))))")
    return parameters
