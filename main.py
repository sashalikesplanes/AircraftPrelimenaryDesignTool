import numpy as np
from conceptualDesign.conceptualDesign import conceptualDesign
from conceptualDesign.wingSizing import wingSizing
from misc.openData import openData

# comment

if __name__ == "__main__":

    parameters = openData("design1")
    print(parameters)
    conceptualDesign(parameters)

# hello world
