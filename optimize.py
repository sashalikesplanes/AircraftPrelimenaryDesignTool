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
    # X = np.array([[2], [1000]])  # compressionratio --> 50 steps
    # Y = np.array([[25], [200]])  # velocity --> 100 steps
    x = np.logspace(0.31, 3, num=50, base=10)  # compression ratio
    y = np.arange(25, 200, 5)  # velocity
    material_data: dict = load_materials()

    matrix = np.zeros((len(x), len(y)))
    print(matrix)

    for index_i, i in enumerate(x):
        for index_j, j in enumerate(y):
            print(f"Hello world! {i} {j}")
            params['compressionRatio'] = i
            params['velocity'] = j

<<<<<<< Updated upstream
            _, result = conceptualDesign(params, material_data, 2)
=======
            _, result = conceptualDesign(params, material_data, 50)
>>>>>>> Stashed changes
            variable = result["fuelMass"]
            matrix[index_i, index_j] = variable.iloc[-1]

    # print(matrix)
    x = np.logspace(0.31, 3, num=51, base=10)  # compression ratio
    y = np.arange(25, 205, 5)  # velocity

    plt.pcolormesh(x, y, matrix)
    plt.show()


if __name__ == "__main__":
    # bnds = [(500, 10000), (2, 1000), (150, None)]
    # print(minimize(func_to_optimize, (5000, 10, 151),
    #       args=(10,), bounds=bnds, method="SLSQP"))
    parameters = openData("design1")
    graph_stuff(parameters)
