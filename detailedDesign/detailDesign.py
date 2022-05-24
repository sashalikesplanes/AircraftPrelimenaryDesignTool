import numpy as np
from pathlib import Path

from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.performAnalyses import perform_analyses
from detailedDesign.getConstraints import get_constraints
from detailedDesign.classes.State import State
from detailedDesign.historicalRelations import get_MTOW_from_historical_relations


def get_ultimate_load_factor():
    GUESS_AT_LOAD_FACTOR = 3
    return GUESS_AT_LOAD_FACTOR


def detail_design():

    # Things that update on sizing - attributes of Aircraft and sub components

    # Things defining the sizing - in /new_designs/config.yaml

    # State in state
    config_file = Path('data', 'new_designs', 'config.yaml')
    aircraft = Aircraft(openData(config_file))
    get_MTOW_from_historical_relations(aircraft)
    aircraft.mtow = get_MTOW_from_historical_relations(aircraft)

    # TODO Create state

    # TODO Loop
    # Magical Disney Loop
    for i in range(2):
        thrust_over_weight, weight_over_surface = 200, 200 # get_constraints(aircraft, State("cruise"))

        ultimate_load_factor = get_ultimate_load_factor()

        aircraft.get_sized(thrust_over_weight, weight_over_surface)

    perform_analyses(aircraft)

    print(aircraft.get_mass())


if __name__ == "__main__":
    detail_design()
