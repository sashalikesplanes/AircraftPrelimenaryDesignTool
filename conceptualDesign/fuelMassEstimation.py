from misc.constants import energyDensityHydrogen


def fuelMassEstimation(params):
    params["fuelMass"] = params["requiredEnergy"] / energyDensityHydrogen
