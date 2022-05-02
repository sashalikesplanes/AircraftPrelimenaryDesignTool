# https://rmi.org/run-on-less-with-hydrogen-fuel-cells/#:~:text=In%20electrical%20terms%2C%20the%20energy,as%20a%20gallon%20of%20diesel.
energyDensityHydrogen = 33.6e3 * 60 * 60  # J/kg


def fuelMassEstimation(params):
    params["fuelMass"] = params["requiredEnergy"] / energyDensityHydrogen
