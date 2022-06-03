#!/usr/bin/python3

from pathlib import Path
from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State


def run_test():
    config_file = Path('data', 'new_designs', 'config.yaml')
    states = {'cruise': State('test_state_engines')}
    aircraft = Aircraft(openData(config_file), states)

    Engines = aircraft.WingGroup.Engines

    # call python file
    states['cruise'].velocity
    states['cruise'].altitude
    aircraft.WingGroup.Wing.span = 120
    aircraft.reference_thrust = 700000


    Engines.size_self()

    print('total mass ', Engines.own_mass*10**(-3),'Tons')
    print('amount of fans', Engines.own_amount_fans)
    print('amount of fans wing', Engines.own_fans_on_wing)
    print('amount of fans fuselage', Engines.own_fans_on_fuselage)

if __name__ == "__main__":
    run_test()
