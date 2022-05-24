#!/usr/bin/python3

from pathlib import Path
from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft
from detailedDesign.classes.State import State


def run_test():
    states_dict = {"cruise": State("cruise")}

    config_file = Path('data', 'new_designs', 'config.yaml')
    aircraft = Aircraft(openData(config_file), states_dict)

    aircraft.reference_area = 10

    aircraft.WingGroup.Wing.size_self()


if __name__ == "__main__":
    run_test()
