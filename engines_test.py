#!/usr/bin/python3

from pathlib import Path
from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State


def run_test():
    config_file = Path('data', 'new_designs', 'config.yaml')
    states = {'cruise': State('test_state_engines'), 'take-off': State('take-off')}
    aircraft = Aircraft(openData(config_file), states)

    Engines = aircraft.WingGroup.Engines

    # call python file
    states['cruise'].velocity
    states['take-off'].velocity
    aircraft.WingGroup.Wing.span = 139
    aircraft.reference_takeoff_thrust = 1800000 #1400000
    aircraft.reference_cruise_thrust = 1000000 # 1Mw


    Engines.size_self()

    print('total mass ', Engines.own_mass*10**(-3),'Tons')
    print('amount of fans', Engines.own_amount_fans)
    print('amount of fans wing', Engines.own_fans_on_wing)
    print('amount of fans fuselage', Engines.own_fans_on_fuselage)
    print("diameter fan", Engines.own_diameter_fan)
    print("tip speed", Engines.own_tip_speed)
    print("length fan", Engines.own_length_fan)

if __name__ == "__main__":
    run_test()
