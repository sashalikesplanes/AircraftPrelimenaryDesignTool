import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from misc.openData import openData
from misc.materials import load_materials
import matplotlib.pyplot as plt
from tqdm import tqdm


material_data: dict = load_materials()


def run_concept(params):

    params, df = conceptualDesign(params, material_data, 100)
    return df["fuelMass"].iloc[-1]


if __name__ == "__main__":
    parameters = openData("design1")

    run_concept(parameters)
    # print(parameters['fuelMass'], parameters["balloonVolume"],
    #       parameters["balloonRadius"], parameters["balloonLength"], parameters["wallThickness"], parameters["balloonStructuralMass"], parameters["wingArea"])
    # print(parameters)
    print(parameters)
    totalEngines = parameters["totalDrag"] * parameters["velocity"] / 2e6
    massBig = parameters["fuselageStructuralMass"] + \
        parameters["balloonStructuralMass"]
    fuelBig = parameters["fuelMass"]

    parameters = openData("design1")
    parameters["compressionRatio"] = 250

    run_concept(parameters)
    print("We need ", massBig / (parameters["fuselageStructuralMass"] +
          parameters["balloonStructuralMass"]), " x more material")
    print("We need ", fuelBig / parameters["fuelMass"], " x more fuel")
