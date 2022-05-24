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

    aircraft.WingGroup.Wing.size_self()

    assert 1 == 2
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1
    assert 1 == 1
    print("WING TESTS PAST")


if __name__ == "__main__":
    run_test()
