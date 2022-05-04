from misc.ISA import getDensity, getPressure
from conceptualDesign.wingSizing import wingSizing
from conceptualDesign.totalMassEstimation import totalMassEstimation
from conceptualDesign.propulsionSizing import propulsionSizing
from conceptualDesign.fuelMassEstimation import fuelMassEstimation
from conceptualDesign.energyRequired import energyRequired
from conceptualDesign.dragModel import dragModel
from conceptualDesign.balloonSizing import balloonSizing
from conceptualDesign.initializeParameters import initializeParameters
from conceptualDesign.fuselageSizing import fuselageWeight
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def conceptualDesign(parameters, material_data, iters):
    """Perform preliminary design using design parameters"""

    # Get the density at the cruise altitude hello world
    rho = getDensity(parameters["altitude"])

    pAir = getPressure(parameters["altitude"])

    df = pd.DataFrame()
    prev_fuel = -100

    initializeParameters(parameters)

    totalMassEstimation(parameters)  # Done
    for i in range(int(iters)):

        # balloon sizing
        balloonSizing(parameters, rho, pAir)  # Done
        if np.isnan(parameters["fuelMass"]):
            # print("Diverged")
            break

        # wing
        wingSizing(parameters, rho)  # Done

        # Fuselage Weight
        fuselageWeight(parameters)

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

        # lst.append(parameters["balloonArea"])
        df = df.append(parameters, ignore_index=True)

        if abs(parameters["fuelMass"]-prev_fuel) < 0.01:
            # print("Converged")
            break
        else:
            prev_fuel = parameters["fuelMass"]

        # # check if converged
        # i += 1

    # plt.plot(range(100), lst)
    # plt.show()
    # print(df)
    # df.plot()
    # plt.show()

    # print(parameters)
    return parameters, df
