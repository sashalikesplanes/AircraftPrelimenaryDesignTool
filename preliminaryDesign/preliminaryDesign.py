import numpy as np
from preliminaryDesign.classes.Aircraft import Aircraft


def preliminaryDesign(file):
    ac = Aircraft(file)
    ac.makeFuselage()


if __name__ == "__main__":
    pass
