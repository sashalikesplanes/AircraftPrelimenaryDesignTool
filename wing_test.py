#!/usr/bin/python3

from pathlib import Path
from misc.openData import openData
from detailedDesign.classes.Aircraft import Aircraft


def run_test():
    config_file = Path('data', 'new_designs', 'config.yaml')
    aircraft = Aircraft(openData(config_file))

    aircraft.reference_area = 10


    aircraft.WingGroup.Wing.size_self()



if __name__ == "__main__":
    run_test()
