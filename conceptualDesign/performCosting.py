pricePerKgCarbonfiber = 60
pricePerKgAlu = 12.22
pricePerPerKgHydrogen = 2.5
staffPerHour = 1250

materialCostContingency = 1.5


def performCosting(params):
    params["materialCosts"] = (params["balloonStructuralMass"] *
                               pricePerKgCarbonfiber + params["wingStructuralMass"] * pricePerKgAlu + params["fuselageStructuralMass"] * pricePerKgAlu) * materialCostContingency
    params["operatingCosts"] = params["fuelMass"] * pricePerPerKgHydrogen + \
        (params["flightRange"] / params["velocity"] / 3600) * staffPerHour
    print(params["fuelMass"], pricePerPerKgHydrogen,
          params["flightRange"], params["velocity"])
    params["balloonLiftRatio"] = params["balloonLift"] / \
        (params["totalMass"] * 9.81)
