import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from misc.openData import openData
from misc.materials import load_materials
import matplotlib.pyplot as plt
from tqdm import tqdm


material_data: dict = load_materials()


def run_concept(params):

<<<<<<< HEAD
    params, df = conceptualDesign(params, material_data, 1000)
=======
    params, df = conceptualDesign(params, material_data, 100)
>>>>>>> 0b966bb199943286e2651233174ee5c6d16b9f6b
    return df["fuelMass"].iloc[-1]


if __name__ == "__main__":
    parameters = openData("design1")

    run_concept(parameters)
    print(parameters['fuelMass'], parameters["balloonVolume"],
          parameters["balloonRadius"], parameters["balloonLength"])
