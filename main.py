import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from misc.openData import openData
from misc.materials import load_materials
import matplotlib.pyplot as plt
from tqdm import tqdm


material_data: dict = load_materials()


def run_concept(params):

    params, df = conceptualDesign(params, material_data, 50)
    return df["fuelMass"].iloc[-1]


if __name__ == "__main__":
    parameters = openData("design1")

    speed = np.arange(50, 300, 10)
    range_list = np.arange(1000000, 10000000, 100000)

    lst = []
    for sped in speed:
        for dist in tqdm(range_list):
            param = parameters.copy()
            param["velocity"] = sped
            param["flightRange"] = dist
            result = run_concept(param)
            if not np.isnan(result):
                lst.append([sped, dist, result])

    matrix = np.array(lst)
    X = matrix[:, 0]
    Y = matrix[:, 1]
    plt.scatter(X, Y)
    plt.show()

    # run_concept(parameters)
