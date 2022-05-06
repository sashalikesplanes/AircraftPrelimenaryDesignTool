from misc.constants import energyDensityHydrogen


def fuelMassEstimation(params):
    # print(params["solarEnergy"]/params["requiredEnergy"])
    params["fuelMass"] = (params["requiredEnergy"] - params["solarEnergy"]) / energyDensityHydrogen
