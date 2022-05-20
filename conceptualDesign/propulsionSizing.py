def propulsionSizing(params):

    enginePower = params["totalDrag"] * params["velocity"] * \
        params["engineEfficiency"] * params["takeOffPowerContingency"]
    fuelCellPower = enginePower * params["fuelCellEfficiency"]

    params["fuelCellPower"] = fuelCellPower

    engine_mass = enginePower / params["engineSpecificPower"]
    fuel_cell_mass = fuelCellPower / params["fuelCellSpecificPower"]

    params["engineMass"] = engine_mass
    params["fuelCellMass"] = fuel_cell_mass
    params["propulsionMass"] = engine_mass + fuel_cell_mass
