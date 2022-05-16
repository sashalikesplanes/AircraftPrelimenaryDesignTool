from conceptualDesign.conceptualDesign import conceptualDesign
from misc.openData import openData
from misc.materials import load_materials
import matplotlib.pyplot as plt
from tqdm import tqdm
# from designSpace import optimize_altitude
import pandas as pd
import json

material_data: dict = load_materials()


def run_concept(params):

    params, df = conceptualDesign(params, material_data, 1000)
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


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


if __name__ == "__main__":

    parameters = openData("design1")
    # print(run_concepts(8e6, [200], [200], specified_altitude=None, params_to_table=[
    # "compressionRatio", "velocity", "fuelMass", "massEfficiency", "totalMass", "balloonVolume", "wingArea", "opCostsPerPax"], alt_bounds=(1000, 6000)))
    df = run_concept(parameters)
    print(parameters["totalDrag"] / (0.5 * 0.7 * 200**2 * 875))
    print(df[
        ['balloonVolume',
         'tailStructuralMass',
         'fuselageLength',
         'meanAerodynamicChord', 'fuselageStructuralMass', 'wingStructuralMass',
         'balloonStructuralMass', 'fuelMass',
         'propulsionMass', 'totalMass', "wingSpan",
         'wingArea', 'totalDrag', ]].iloc[-20:])
    pretty(parameters)

    # plt.plot(range(len(df.index)), df["fuelMass"])
    # plt.show()

    # print(run_concepts(8E6, [200], [250], specified_altitude=11000, params_to_table=[
    #       "compressionRatio", "velocity", "fuelMass", "totalMass", "balloonVolume"]))

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
