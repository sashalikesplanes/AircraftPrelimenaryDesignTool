import numpy as np
from preliminaryDesign.preliminaryDesign import preliminaryDesign
from preliminaryDesign.wingSizing import wingSizing
from misc.openData import openData

# comment

if __name__ == "__main__":

    parameters = openData("design1")
    print(parameters)
    preliminaryDesign(parameters)

# hello world
