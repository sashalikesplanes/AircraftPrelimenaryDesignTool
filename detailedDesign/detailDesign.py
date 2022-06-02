import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt

from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.performAnalyses import perform_analyses
from detailedDesign.getConstraints import get_constraints
from detailedDesign.classes.State import State
from detailedDesign.historicalRelations import get_MTOM_from_historical_relations
from detailedDesign.log import setup_custom_logger
from detailedDesign.potatoPlot import make_potato_plot
from detailedDesign.flightEnvelope import make_flight_envelope
from detailedDesign.sketch import sketch_aircraft


def get_ultimate_load_factor():
    # N_max_des = None # from maneuver/gust diagram
    # N_ult = 1.5*N_max_des # CS25 reg (sam's summaries)
    GUESS_AT_LOAD_FACTOR = 3.75 
    return GUESS_AT_LOAD_FACTOR


def detail_design(debug=False):
    logger = setup_custom_logger("logger", debug)
    states = {"cruise": State('cruise'), "take-off": State('take-off')}

    # State in state
    config_file = Path('data', 'new_designs', 'config.yaml')
    aircraft = Aircraft(openData(config_file), states, debug=True)

    aircraft.mtom = get_MTOM_from_historical_relations(aircraft)
    previous_mtom = 0  # For checking convergence
    lst = [aircraft.mtom]

    # Size the cabin and cargo bay as it is constant and is a dependency for other components
    pre_run = aircraft.FuselageGroup.Fuselage
    pre_run.Cabin.size_self()
    pre_run.CargoBay.size_self()

    for i in range(1000):
        get_constraints(aircraft)
        aircraft.ultimate_load_factor = get_ultimate_load_factor()

        aircraft.get_sized()

        lst.append(aircraft.mtom)
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

    plt.figure(1)
    plt.plot(range(len(lst)), lst, "o-")
    plt.xlabel("Iterations [-]")
    plt.ylabel("Maximum take-off mass [kg]")
    plt.title("MTOM over iterations")

    sketch_aircraft(aircraft)

    print(f"Aircraft CG: {aircraft.get_cg()}")

    # make_potato_plot(aircraft)
    perform_analyses(aircraft)
    # make_flight_envelope(aircraft, "cruise")
    # make_flight_envelope(aircraft, "take-off")
    # aircraft.WingGroup.Wing.size_AR(aircraft)
    make_potato_plot(aircraft)


if __name__ == "__main__":
    detail_design(debug=True)
