def energyRequired(params):
    params["requiredEnergy"] = params["totalDrag"] * \
        params["flightRange"] / params["propEfficiency"]
