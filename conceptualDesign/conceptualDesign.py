import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

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


def conceptualDesign(parameters, material_data):
    """Perform preliminary design using design parameters"""

    # Get the density at the cruise altitude hello world
    rho = getDensity(parameters["altitude"])
    dp = abs(getPressure(1000) - getPressure(parameters["altitude"]))
    pAir = getPressure(parameters["altitude"])

    df = pd.DataFrame()

    payloadMassEstimation(parameters)  # Done
    fuselageSizing(parameters, dp)  # Done

    totalMassEstimation(parameters)  # Done
    # i = 0
    lst = []
    for i in range(1000):
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
        # lst.append(parameters["balloonArea"])
        df = df.append(parameters, ignore_index=True)

        # # check if converged
        # i += 1

    # plt.plot(range(100), lst)
    # plt.show()
    print(df)
    df.plot()
    plt.show()

    # print(parameters)
    return parameters, df
