import numpy as np
from pathlib import Path

from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.performAnalyses import perform_analyses
from detailedDesign.getConstraints import get_constraints
from detailedDesign.classes.State import State
from detailedDesign.historicalRelations import get_MTOM_from_historical_relations
import logging


def get_ultimate_load_factor():
    # N_max_des = None # from maneuver/gust diagram
    # N_ult = 1.5*N_max_des # CS25 reg (sam's summaries)
    GUESS_AT_LOAD_FACTOR = 3
    return GUESS_AT_LOAD_FACTOR


def detail_design(debug=False):

    logging.basicConfig()
    logger = logging.getLogger('main_logger')
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    states = {"cruise": State('cruise')}

    # Things that update on sizing - attributes of Aircraft and sub components

    # Things defining the sizing - in /new_designs/config.yaml

    # State in state
    config_file = Path('data', 'new_designs', 'config.yaml')
    aircraft = Aircraft(openData(config_file), states, debug=True)
    aircraft.mtom = get_MTOM_from_historical_relations(aircraft)
    previous_mtom = aircraft.mtom  # For checking convergence
    pre_run = aircraft.FuselageGroup.Fuselage
    pre_run.Cabin.size_self()
    pre_run.CargoBay.size_self()

    # TODO Loop
    # Magical Disney Loop
    while True:
        get_constraints(aircraft)

        aircraft.ultimate_load_factor = get_ultimate_load_factor()

        aircraft.get_sized()
        if debug:
            print(f"{ aircraft.mtom = }")
        # Check divergence
        if np.isnan(aircraft.mtom):
            break

        # Check convergence
        if aircraft.mtom - previous_mtom < 5:
            print("CONVERGED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            break
        previous_mtom = aircraft.mtom

    perform_analyses(aircraft)

    print(
        f"MTOM = {aircraft.mtom} kg, OEM = {aircraft.oem} kg, Fuel Mass = {aircraft.fuel_mass}")


if __name__ == "__main__":
    detail_design(debug=True)
