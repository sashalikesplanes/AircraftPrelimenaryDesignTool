import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State
from detailedDesign.potatoPlot import make_potato_plot
from detailedDesign.sketch import sketch_aircraft
from detailedDesign.run_aircraft import run_aircraft
from detailedDesign.carrotPlot import make_carrot_plot
from detailedDesign.classes.Stability_draft import get_xplot


# def get_ultimate_load_factor():
#     # N_max_des = None # from maneuver/gust diagram
#     # N_ult = 1.5*N_max_des # CS25 reg (sam's summaries)
#     GUESS_AT_LOAD_FACTOR = 3.75
#     return GUESS_AT_LOAD_FACTOR


def detail_design(debug=False):
    # State in state
    states = {"cruise": State('cruise'), "take-off": State('take-off')}
    config_file = Path('data', 'new_designs', 'config.yaml')
    aircraft = Aircraft(openData(config_file), states, debug=debug)

    run_aircraft(aircraft, debug=debug)
    print("DONE")

    # ########################################### #
    # ##   MAKE ALL THE COOL PLOTS AND STUFF   ## #
    # ########################################### #
    # sketch_aircraft(aircraft)
    # make_potato_plot(aircraft, debug=debug)
    # print(f"Aircraft CG: {aircraft.get_cg()}")
    # perform_analyses(aircraft)
    # make_flight_envelope(aircraft, "cruise")
    # make_flight_envelope(aircraft, "take-off")
    # aircraft.WingGroup.Wing.size_AR(aircraft)

    df = make_carrot_plot()
    f_stab, f_cont = get_xplot(aircraft)

    plt.figure(5)
    y_min = 1e6
    z_min = None
    for row in np.array(df):
        z = row[1]
        x1 = row[2]
        x2 = row[3]
        y1 = f_cont(row[2])
        y2 = f_stab(row[3])
        if y1 > y2:
            y = y1
        else:
            y = y2

        if y < y_min:
            y_min = y
            z_min = z
        plt.plot([x1, x2], [y, y], "--")

    print(f"Best Sh/S: {y_min}, best Xlemac/Lfus: {z_min}")
    plt.show()


if __name__ == "__main__":
    detail_design(debug=True)
