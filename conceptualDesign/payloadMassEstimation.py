def payloadMassEstimation(params):
    params["payloadMass"] = params["cargoMass"] + params["passengers"] * params["passengerMass"]
