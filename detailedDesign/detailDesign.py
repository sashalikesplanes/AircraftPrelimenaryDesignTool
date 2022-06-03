from pathlib import Path

from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State
from detailedDesign.run_aircraft import run_aircraft
from detailedDesign.performAnalyses import perform_analyses
# from detailedDesign.classes.Wing import sizing_ailerons

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

    # ########################################### #
    # ##   MAKE ALL THE COOL PLOTS AND STUFF   ## #
    # ########################################### #

    perform_analyses(aircraft)
    # make_flight_envelope(aircraft, "cruise")
    # make_flight_envelope(aircraft, "take-off")
    # aircraft.WingGroup.Wing.size_AR(aircraft)
    # aircraft.WingGroup.Wing.sizing_ailerons()
    aircraft.FuselageGroup.Tail.VerticalTail.size_self_geometry()