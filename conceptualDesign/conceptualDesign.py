from misc.ISA import getDensity, getTemperature

from conceptualDesign.wingSizing import wingSizing
from conceptualDesign.totalMassEstimation import totalMassEstimation
from conceptualDesign.propulsionSizing import propulsionSizing
from conceptualDesign.fuelMassEstimation import fuelMassEstimation
from conceptualDesign.energyRequired import energyRequired
from conceptualDesign.dragModel import dragModel
from conceptualDesign.initializeParameters import initializeParameters
from conceptualDesign.fuselageSizing import fuselageWeight
from conceptualDesign.postSizingCalcs import post_sizing_calcs
from conceptualDesign.marketStuff import marketStuff

import pandas as pd
import numpy as np
import warnings
# Ignore warnings from pd.append
warnings.simplefilter(action='ignore', category=FutureWarning)


def conceptualDesign(parameters, material_data, iters):
    """Perform preliminary design using design parameters"""
    converged = False

    # Get the density at the cruise altitude hello world
    rho = getDensity(parameters["altitude"])
    temp = getTemperature(parameters["altitude"])

    df = pd.DataFrame()
    prev_fuel = -100

    initializeParameters(parameters)

    for _ in range(int(iters)):
        if np.isnan(parameters["fuelMass"]):
            print("Diverged")
            break

        # wing
        wingSizing(parameters, rho)

        # Fuselage Weight
        fuselageWeight(parameters)

        # drag model
        dragModel(parameters, rho, temp)

        # propulsion sizing
        propulsionSizing(parameters)

        # energy required
        energyRequired(parameters)

        # fuel mass estimation
        fuelMassEstimation(parameters)

        # total mass
        totalMassEstimation(parameters)

        # add current iteration to dataframe in order to track convergence/divergence behaviour
        df = df.append(parameters, ignore_index=True)

        if abs(parameters["fuelMass"] - prev_fuel) < 0.01:
            converged = True
            break
        else:
            prev_fuel = parameters["fuelMass"]

    if converged:
        print("running post")
        marketStuff(parameters)
        post_sizing_calcs(parameters)

    return parameters, df
