import numpy as np


def preliminaryDesign(parameters):
    """Perform preliminary design using design parameters"""

    fuselageSizing(parameters)


    rho = # get rho from isa function

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

        # energy required

        # fuel mass estimation

        # total mass

        # check if converged

        i += 1

    return parameters
