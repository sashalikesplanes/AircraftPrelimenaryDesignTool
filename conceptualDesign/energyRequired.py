def energyRequired(params):
    E_req = params["totalDrag"] * \
        params["flightRange"] / params["propEfficiency"]
    params["requiredEnergy"] = E_req * params["propulsionContingency"]
