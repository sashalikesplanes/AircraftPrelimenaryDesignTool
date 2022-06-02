import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.run_aircraft import run_aircraft
from detailedDesign.classes.State import State
from misc.openData import openData
from detailedDesign.potatoPlot import make_potato_plot


def make_carrot_plot():
    debug = False
    states = {"cruise": State('cruise'), "take-off": State('take-off')}

    max_length = 100
    x_lemacs = np.arange(0, max_length)

    lst = []
    for x_lemac in x_lemacs:
        # print(f"Starting {x_lemac}")
        config_file = Path('data', 'new_designs', 'config.yaml')
        aircraft = Aircraft(openData(config_file), states, debug=debug)
        aircraft.x_lemac = x_lemac

        run_aircraft(aircraft)
        # print("Getting CGs")
        cg_range = make_potato_plot(aircraft, debug=debug)
        x_lemac_over_l_fus = x_lemac / aircraft.FuselageGroup.Fuselage.length

        lst.append([x_lemac_over_l_fus, cg_range[0], cg_range[1]])
        # print(f"Finished {x_lemac}")

    header = ["pos", "fw cg", "aft cg"]
    df = pd.DataFrame(np.array(lst), columns=header)

    plt.figure(4)
    plt.plot(df["fw cg"], df["pos"])
    plt.plot(df["aft cg"], df["pos"])
    plt.show(4)

    return df
