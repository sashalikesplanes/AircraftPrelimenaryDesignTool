pricePerKgCarbonfiber = 60
pricePerKgAlu = 12.22
pricePerPerKgHydrogen = 2.5
staffPerHour = 1250

materialCostContingency = 1.5

power_per_engine = 2e6  # [W]


def post_sizing_calcs(params):
    params["materialCosts"] = (params["balloonStructuralMass"] *
                               pricePerKgCarbonfiber + params["wingStructuralMass"] * pricePerKgAlu + params["fuselageStructuralMass"] * pricePerKgAlu) * materialCostContingency
    params["operatingCosts"] = params["fuelMass"] * pricePerPerKgHydrogen + \
        (params["flightRange"] / params["velocity"] / 3600) * staffPerHour

    params["balloonLiftRatio"] = params["balloonLift"] / \
        (params["totalMass"] * 9.81)

    params["opCostsPerPax"] = params["operatingCosts"] / params["passengers"]

    params["numOfEngines"] = params["totalDrag"] * \
        params["velocity"] / power_per_engine

    params["massEfficiency"] = params["payloadMass"] / params["totalMass"]
