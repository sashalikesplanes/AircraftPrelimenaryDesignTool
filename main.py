import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from conceptualDesign.wingSizing import wingSizing
from misc.openData import openData
from misc.materials import load_materials

# comment

if __name__ == "__main__":

    material_data: dict = load_materials()

    parameters = openData("design1")

    conceptualDesign(parameters, material_data)
    print(parameters)

# hello world
