def totalMassEstimation(params):
    params["totalMass"] = params["liftingHydrogenMass"] + params["fuelMass"] + params["payloadMass"] + \
        params["propulsionMass"] + params["fuselageStructuralMass"] + \
        params["wingStructuralMass"] + \
        params["balloonStructuralMass"] + params["solarMass"]
