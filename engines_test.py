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
    aircraft.WingGroup.Wing.span = 100
    aircraft.reference_thrust = 53500 * 4.44822 * 4
    aircraft.FuselageGroup.Fuselage.diameter = 6

    Engines.size_self()

    print('total mass ', Engines.own_mass)
    print('amount of propellors', Engines.own_amount_prop)


if __name__ == "__main__":
    run_test()
