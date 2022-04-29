import numpy as np

from preliminaryDesign.balloonSizing import balloonSizing
from preliminaryDesign.dragModel import dragModel
from preliminaryDesign.energyRequired import energyRequired
from preliminaryDesign.fuelMassEstimation import fuelMassEstimation
from preliminaryDesign.fuselageSizing import fuselageSizing
from preliminaryDesign.propulsionSizing import propulsionSizing
from preliminaryDesign.totalMassEstimation import totalMassEstimation
from preliminaryDesign.wingSizing import wingSizing

from misc.ISA import getDensity


def preliminaryDesign(parameters):
    """Perform preliminary design using design parameters"""

    fuselageSizing(parameters)

    rho = getDensity(parameters["altitude"])


    parameters["totalMass"] = parameters["fuselageMass"]

    i = 0
    while i < 10000:
        # wing
        wingSizing(parameters, rho)

        # balloon sizing
        balloonSizing(parameters, rho)

        # drag model
        dragModel(parameters, rho)

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
