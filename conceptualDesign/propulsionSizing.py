def propulsionSizing(params):

    enginePower = params["totalDrag"] * params["velocity"] * params["engineEfficiency"]
    fuelCellPower = enginePower * params["fuelCellEfficiency"]

    params["propulsionMass"] = enginePower / params["engineSpecificPower"] + \
        fuelCellPower / params["fuelCellSpecificPower"]
