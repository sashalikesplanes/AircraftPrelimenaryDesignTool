from tqdm import tqdm

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


def graph_stuff():
    # altitude = 5000
    # X = np.array([[2], [1000]])  # compressionratio --> 50 steps
    # Y = np.array([[25], [200]])  # velocity --> 100 steps
    x = np.logspace(0.31, 3, num=50, base=10)  # compression ratio
    y = np.arange(60, 300, 5)  # velocity
    material_data: dict = load_materials()

    matrix = np.zeros((len(x), len(y)))
    print(matrix)

    for index_i, i in tqdm(enumerate(x)):
        for index_j, j in tqdm(enumerate(y)):
            params = openData("design1")
            # print(f"Hello world! {i} {j}")
            params['compressionRatio'] = i
            params['velocity'] = j

            _, result = conceptualDesign(params, material_data, 10)
            variable = result["fuelMass"]
            matrix[index_i, index_j] = variable.iloc[-1]
            # print(variable.iloc[-1])

    print(np.count_nonzero(np.isnan(matrix)))
    x = np.logspace(0.31, 3, num=51, base=10)  # compression ratio
    y = np.arange(60, 305, 5)  # velocity

    matrix = np.log(matrix)
    plt.pcolormesh(y, x, matrix)
    plt.show()


if __name__ == "__main__":
    bnds = [(1000, 10999), (5, 100), (20, 330)]  # height, CR, speed
    print(minimize(func_to_optimize, (5000, 20, 80),
          args=(10,), bounds=bnds, method="SLSQP"))
    # graph_stuff()
