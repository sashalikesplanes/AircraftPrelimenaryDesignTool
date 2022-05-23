from detailedDesign.classes.Aircraft import Aircraft
from misc.openData import openData
from pathlib import Path


def detailDesign():

    config = openData(Path('..', 'data', 'new_designs', 'config.yaml'))
    aircraft = Aircraft(config)
    print("Bye World!")
    print(aircraft.test_prop, aircraft.FuselageGroup.test_prop_fuselage)


if __name__ == "__main__":
    detailDesign()
