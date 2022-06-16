import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from detailedDesign.historicalRelations import get_MTOM_from_historical_relations
from detailedDesign.log import setup_custom_logger
from detailedDesign.getConstraints import get_constraints

name = os.getlogin()
if name == "Devoteam":
    logger = setup_custom_logger("logger", False)
else:
    logger = setup_custom_logger("logger", True)


def run_aircraft(aircraft, debug=False):

    aircraft.mtom = get_MTOM_from_historical_relations(aircraft)
    previous_mtom = 0
    header = aircraft.make_mass_lst()[1]
    lst = [aircraft.make_mass_lst()[0]]

    # Size the cabin and cargo bay as it is constant and is a dependency for other components
    pre_run = aircraft.FuselageGroup.Fuselage
    pre_run.Cabin.size_self()
    pre_run.CargoBay.size_self()

    for i in range(1000):
        get_constraints(aircraft)

        aircraft.get_sized()

        lst.append(aircraft.make_mass_lst()[0])
        # Check divergence
        if np.isnan(aircraft.mtom):
            logger.warn("DIVERGED :(")
            break
        # Check convergence
        if abs(aircraft.mtom - previous_mtom) < 0.01:
            logger.warn("CONVERGED :)")
            logger.debug(f"Took {i} iterations")
            break
        previous_mtom = aircraft.mtom

    aircraft.get_cged()

    # if True:
    #     df = pd.DataFrame(lst, columns=header)
    #     df.loc[:, ["Miscellaneous", "VerticalTail", "HorizontalTail", "AssFuelContainer", "AftFuelContainer", "ForwardFuelContainer", "Fuselage", "FuelCells", "Engines", "Wing", "Aircraft"]].plot(style="o-")
    #
    #     # y = [x[1] for x in lst]
    #     # plt.plot(range(len(lst)), y, "ro-", label=header[1])
    #     # y = [x[2] for x in lst]
    #     # plt.plot(range(len(lst)), y, "go-", label=header[2])
    #     # print(df)
    #     plt.xlabel("Iterations [-]")
    #     plt.ylabel("System Mass [kg]")
    #     plt.title("MTOM over iterations")
    #     # plt.ylim([0, 10e9])
    #     # plt.yscale("log")
    #     plt.legend()
    #     plt.show()

    return aircraft
