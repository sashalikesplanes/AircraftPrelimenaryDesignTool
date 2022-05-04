from cmath import nan
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


def optimize_altitude_cr(opt_params, iters):
    altitude, compressionRatio = opt_params
    material_data: dict = load_materials()

    parameters = openData("design1")

    parameters['altitude'] = altitude
    parameters['compressionRatio'] = compressionRatio
    conceptualDesign(parameters, material_data, iters)
    return parameters['fuelMass']


def optimize_cr(opt_params, iters, velocity, range):
    altitude, compressionRatio = opt_params
    material_data: dict = load_materials()

    parameters = openData("design1")

    parameters['velocity'] = velocity
    parameters['flightRange'] = range

    parameters['altitude'] = altitude
    parameters['compressionRatio'] = compressionRatio
    conceptualDesign(parameters, material_data, iters)
    return parameters['fuelMass']


def graph_stuff(steps, iters, velocityStart, velocityEnd, rangeEnd, rangeStart, maxCR, file_name):
    rangeSteps = np.linspace(
        rangeEnd, rangeStart, num=steps)  # compression ratio
    velocitySteps = np.linspace(
        velocityStart, velocityEnd, num=steps)  # velocity
    # material_data: dict = load_materials()

    matrix = np.zeros((len(rangeSteps), len(velocitySteps)))

    for index_i, range in tqdm(enumerate(rangeSteps)):
        for index_j, velocity in enumerate(velocitySteps):

            bnds = [(500, 10000), (2, 700)]
            optimization = minimize(optimize_cr, (5000, 10),
                                    args=(25, velocity, range), bounds=bnds, method="SLSQP")
            CR = optimization.x[1]
            value = optimization.fun

            # params = openData("design1")
            # # # print(f"Hello world! {i} {j}")
            # params["flightRange"] = range
            # params["velocity"] = velocity
            # params['compressionRatio'] = compRatio
            # params['altitude'] = altitude
            # _, result = conceptualDesign(params, material_data, iters)

            # variable = result["fuelMass"]
            if np.isnan(value):
                matrix[index_i, index_j] = None
            else:
                matrix[index_i, index_j] = CR

    rangeSteps = np.linspace(
        rangeEnd, rangeStart, num=steps + 1)
    velocitySteps = np.linspace(
        velocityStart, velocityEnd, num=steps + 1)  # velocity
    # rangeSteps, velocitySteps = np.meshgrid(rangeSteps, velocitySteps)
    # matrix = np.nan_to_num(matrix, nan=np.nanmax(matrix) * 1000)
    print(rangeSteps.shape, velocitySteps.shape, matrix.shape)
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    print(matrix)
    np.save(file_name, matrix)
    # ax.plot_surface(rangeSteps, velocitySteps, np.log(matrix))
    # plt.pcolormesh(velocitySteps, rangeSteps, np.log(matrix))
    # plt.show()


if __name__ == "__main__":
    # bnds = [(500, 10000), (5, 700), (100, None)]
    # print(minimize(func_to_optimize, (5000, 100, 150),
    #       args=(25,), bounds=bnds, method="SLSQP").fun)
    graph_stuff(50, 25, 30, 150, 5000000, 10000000,
                5, "graphData/comp-ratios")
    # graph_stuff(50, 25, 30, 150, 5000000, 10000000,
    #            700, "graphData/plane-mode")
    # bnds = [(500, 10000), (2, 700)]
    # optimization = minimize(optimize_cr, (5000, 10),
    #                         args=(25, 1000, 5e10), bounds=bnds, method="SLSQP")
