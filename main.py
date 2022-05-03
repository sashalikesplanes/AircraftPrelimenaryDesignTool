import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from conceptualDesign.wingSizing import wingSizing
from misc.openData import openData
from misc.materials import load_materials
import matplotlib.pyplot as plt

# comment

if __name__ == "__main__":

    material_data: dict = load_materials()

    parameters = openData("design1")

    lst = []
    for i in range(100):
        params = parameters.copy()
        params["altitude"] = i * 100
        params, _ = conceptualDesign(params, material_data, 50)

        lst.append(params["totalMass"])

    y = [100 * x for x in range(100)]
    plt.plot(y, lst)
    plt.show()

    parameters, df = conceptualDesign(parameters, material_data)
    print(parameters)

# hello world
