from detailedDesign.classes.Aircraft import Aircraft
from misc.openData import openData
from pathlib import Path


def get_ultimate_load_factor():
    GUESS_AT_LOAD_FACTOR = 3
    return GUESS_AT_LOAD_FACTOR


def detail_design():

    # Things that update on sizing - attributes of Aircraft and sub components

    # Things defining the sizing - in /new_designs/config.yaml

    # State in state

    # TODO Historical Relations

    # TODO Create state

    config = openData(Path('..', 'data', 'new_designs', 'config.yaml'))
    aircraft = Aircraft(config)

    # TODO Loop
    for i in range(10):
        thrust_over_weight, weight_over_surface = get_constraints(
            aircraft, state)

        ultimate_load_factor = get_ultimate_load_factor()

        aircraft.get_sized(thrust_over_weight, weight_over_surface)

    perform_analyses(aircraft)


if __name__ == "__main__":
    detail_design()
