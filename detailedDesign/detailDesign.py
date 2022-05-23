from detailedDesign.classes.Aircraft import Aircraft
from misc.openData import openData
import pathlib import Path


def detailDesign():

    config = openData(Path('.', 'data', 'new_designs', 'config.yaml'))
    aircraft = Aircraft(config)
    print("Bye World!")

    print(aircraft.WingGroup.Engines.count)


if __name__ == "__main__":
    detailDesign()
