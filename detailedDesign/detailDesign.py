from detailedDesign.classes.Aircraft import Aircraft
from misc.openData import openData
from pathlib import Path


def detailDesign():

    config = openData(Path('..', 'data', 'new_designs', 'config.yaml'))
    aircraft = Aircraft(config)
    print(aircraft.FuselageGroup.Power.Batteries.test_prop)


if __name__ == "__main__":
    detailDesign()
