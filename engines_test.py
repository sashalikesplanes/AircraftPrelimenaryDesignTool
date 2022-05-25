#!/usr/bin/python3

from pathlib import Path
from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State


def run_test():
    config_file = Path('data', 'new_designs', 'config.yaml')
    states = {"cruise": State('cruise')}
    aircraft = Aircraft(openData(config_file), states)

    Engines = aircraft.WingGroup.Engines

    # call python file
    aircraft.WingGroup.Wing.span = 10

    Engines.size_self()

    print(Engines.own_mass)

    # print
    # print(mass_H2)


if __name__ == "__main__":
    run_test()
