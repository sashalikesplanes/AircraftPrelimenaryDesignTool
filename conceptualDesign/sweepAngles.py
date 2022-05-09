import numpy as np


def convertSweep(quarterChordSweep, desiredPercentile, taperRatio, aspectRatio):

    return np.arctan(
        np.tan(quarterChordSweep) - 4/aspectRatio*((desiredPercentile-25)/100) * (1 - taperRatio)/(1 + taperRatio))
