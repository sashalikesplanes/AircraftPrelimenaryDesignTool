def propulsionSizing(params):

    enginePower = params["totalDrag"] * params["velocity"] * \
        params["engineEfficiency"] * params["takeOffPowerContingency"]
    fuelCellPower = enginePower * params["fuelCellEfficiency"]

    params["propulsionMass"] = enginePower / params["engineSpecificPower"] + \
        fuelCellPower / params["fuelCellSpecificPower"]
