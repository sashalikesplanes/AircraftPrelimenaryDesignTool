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


if __name__ == "__main__":
    bnds = [(1000, 10999), (4.99, 20), (100, 150)]  # height, CR, speed
    print(minimize(func_to_optimize, (4000, 9, 140),
          args=(30,), bounds=bnds, method="SLSQP"))
    # graph_stuff()
