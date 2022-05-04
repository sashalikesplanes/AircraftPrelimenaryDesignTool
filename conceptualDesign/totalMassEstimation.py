def totalMassEstimation(params):
    # Add up all the main masses
    params["totalMass"] = params["liftingHydrogenMass"] + params["fuelMass"] + params["payloadMass"] + \
        params["propulsionMass"] + params["fuselageStructuralMass"] + \
        params["wingStructuralMass"] + params["balloonStructuralMass"]
