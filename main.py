
import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from misc.openData import openData
from misc.materials import load_materials
import matplotlib.pyplot as plt
from tqdm import tqdm
from designSpace import optimize_altitude
import pandas as pd


material_data: dict = load_materials()


def run_concept(params):

    params, df = conceptualDesign(params, material_data, 100)
    # return df["fuelMass"].iloc[-1]
    return df


def run_concepts(design_range,
                 design_speeds,
                 comp_ratios,
                 specified_altitude,
                 params_to_table=["compressionRatio", "fuelMass"],
                 iters=1000,
                 alt_bounds=(1000, 10999)):
    """
    Run several different compression ratio concepts at the design range and speed. Receive a table with the params_to_table
    at the end of the iterations
    """
    out_table = pd.DataFrame()
    for (design_speed, comp_ratio) in tqdm(zip(design_speeds, comp_ratios)):

        params = openData("design1")

        if not specified_altitude:
            altitude = optimize_altitude(
                design_speed, comp_ratio, design_range, bnds=[alt_bounds])
            params["altitude"] = altitude
        else:
            params["altitude"] = specified_altitude

        params["velocity"] = design_speed
        params["flightRange"] = design_range
        params["compressionRatio"] = comp_ratio

        params, _ = conceptualDesign(params, material_data, iters)
        out_table = out_table.append(params, ignore_index=True)

    return out_table[params_to_table]


if __name__ == "__main__":
    parameters = openData("design1")
    # print(run_concepts(8e6, [200], [200], specified_altitude=None, params_to_table=[
          # "compressionRatio", "velocity", "fuelMass", "massEfficiency", "totalMass", "balloonVolume", "wingArea", "opCostsPerPax"], alt_bounds=(1000, 6000)))
    df = run_concept(parameters)
    print(df)

    plt.plot(range(len(df.index)), df["fuelMass"])
    plt.show()

    # Show that the design is Poorly
    # parameters = openData("design1")
    # run_concept(parameters)
    # totalEngines = parameters["totalDrag"] * parameters["velocity"] / 2e6
    # massBig = parameters["fuselageStructuralMass"] + \
    #     parameters["balloonStructuralMass"]
    # fuelBig = parameters["fuelMass"]

    # parameters = openData("design1")
    # parameters["compressionRatio"] = 250

    # run_concept(parameters)
    # print("We need ", massBig / (parameters["fuselageStructuralMass"] +
    #       parameters["balloonStructuralMass"]), " x more material")
    # print("We need ", fuelBig / parameters["fuelMass"], " x more fuel")
