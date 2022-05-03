import imp

import matplotlib.pyplot as plt
from scipy.optimize import minimize, Bounds
from conceptualDesign.conceptualDesign import conceptualDesign
from misc.openData import openData
from misc.materials import load_materials
import numpy as np


def func_to_optimize(params, iters):

    altitude, compressionRatio, velocity = params
    material_data: dict = load_materials()

    parameters = openData("design1")

    parameters['altitude'] = altitude
    parameters['compressionRatio'] = compressionRatio
    parameters['velocity'] = velocity
    conceptualDesign(parameters, material_data, iters)
    print(parameters['fuelMass'], altitude, compressionRatio, velocity)
    return parameters['fuelMass']


def graph_stuff(params):
    # altitude = 5000
    X = np.array([[2], [51]])  # compressionratio --> 50 steps
    Y = np.array([[40], [140]])  # velocity --> 100 steps
    x = np.arange(2, 51)
    y = np.arange(40, 140)
    material_data: dict = load_materials()

    matrix = np.zeros((49, 100))
    print(matrix)

    for i in x:
        for j in y:
            parameters['compressionRatio'] = i
            parameters['velocity'] = j

            _, result = conceptualDesign(params, material_data, 250)
            variable = result["fuelMass"]
            matrix[i, j] = variable.iloc[-1]

    print(matrix)
    plt.pcolormesh()


if __name__ == "__main__":
    # bnds = [(500, 10000), (2, 1000), (150, None)]
    # print(minimize(func_to_optimize, (5000, 10, 151),
    #       args=(10,), bounds=bnds, method="SLSQP"))
    parameters = openData("design1")
    graph_stuff(parameters)
