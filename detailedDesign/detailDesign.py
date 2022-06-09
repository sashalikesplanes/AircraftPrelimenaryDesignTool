from pathlib import Path

from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State
from detailedDesign.run_aircraft import run_aircraft
from detailedDesign.performAnalyses import perform_analyses
from detailedDesign.design_structure import design_structure

# def get_ultimate_load_factor():
#     # N_max_des = None # from maneuver/gust diagram
#     # N_ult = 1.5*N_max_des # CS25 reg (sam's summaries)
#     GUESS_AT_LOAD_FACTOR = 3.75
#     return GUESS_AT_LOAD_FACTOR


def detail_design(debug=False, make_stability=False):
    # State in state
    states = {"cruise": State('cruise'), "take-off": State('take-off')}
    config_file = Path('data', 'new_designs', 'config.yaml')
    aircraft = Aircraft(openData(config_file), states, debug=debug)

    # Stage 1: High level design
    run_aircraft(aircraft, debug=debug)

    # Stage 2: Analyse the things
    # make_stability = True
    perform_analyses(aircraft, make_stability)

    # Stage 3: Sort of detailed design
    design_structure(aircraft)

