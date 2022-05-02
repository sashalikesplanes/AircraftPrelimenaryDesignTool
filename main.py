import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from conceptualDesign.wingSizing import wingSizing
from misc.openData import openData
from misc.materials import load_materials

# comment

if __name__ == "__main__":

    material_data: dict = load_materials()

    parameters = openData("design1")

    for i in range(50):
        params = parameters.copy()
        compression_ratio = i/10 + 0.1
        params["compressionRatio"] = compression_ratio

    parameters, df = conceptualDesign(parameters, material_data)
    print(parameters)

# hello world
