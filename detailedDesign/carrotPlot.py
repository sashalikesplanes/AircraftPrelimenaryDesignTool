import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.run_aircraft import run_aircraft
from detailedDesign.classes.State import State
from misc.openData import openData
from detailedDesign.potatoPlot import make_potato_plot


def make_carrot_plot(force_run=False):
    debug = False
    states = {"cruise": State('cruise'), "take-off": State('take-off')}

    df_location = Path('data', 'dataframes', 'carrot.dat')

    try:
        if force_run:
            raise FileNotFoundError
        df = pd.read_csv(df_location)
    except FileNotFoundError:
        print("Didn't find file requested, generating new one.")
        max_length = 100
        # x_lemacs = np.linspace(40, 80, 8)
      #
        x_lemacs = [55]
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

            lst.append([x_lemac_over_l_fus, cg_range[0], cg_range[1], x_lemac])
            # print(f"Finished {x_lemac}")

        header = ["pos", "fw cg", "aft cg", "xlemac"]
        df = pd.DataFrame(np.array(lst), columns=header)
        df.to_csv(df_location)

    plt.plot(df["fw cg"], df["pos"])
    plt.plot(df["aft cg"], df["pos"])
    plt.xlabel("Xcg/MAC [%]")
    plt.ylabel("Xlemac/Lfus [%]")
    plt.title("Centra of Gravity Range")
    plt.grid()
    plt.savefig(Path("plots", "carrot.png"))
    plt.show()
    plt.close()
    print(df)

    return df
