#!/usr/bin/python3

from pathlib import Path
from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State


def run_test():
    config_file = Path('data', 'new_designs', 'config.yaml')
    states = {"cruise": State('cruise')}
    aircraft = Aircraft(openData(config_file), states)

    aircraft.reference_area = 10

    #init parameters
    aircraft.FuselageGroup.Fuselage.inner_diameter = None

    #call python file
    aircraft.FuselageGroup.Fuselage.FuelContainer.size_self()

    #print
    print(aircraft.FuselageGroup.Fuselage.FuelContainer.thickness)




if __name__ == "__main__":
    run_test()
