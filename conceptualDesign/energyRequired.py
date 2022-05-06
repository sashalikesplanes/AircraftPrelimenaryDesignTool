def energyRequired(params):
    E_req = params["totalDrag"] * \
        params["flightRange"] / params["propEfficiency"]
    params["requiredEnergy"] = E_req

    if params["hasSolarPanels"]:
        S_solar = params["balloonLength"] * params["balloonRadius"]
        # Using HES flexible array
        print(f"Solar area: {S_solar} m^2")
        P_solar = (S_solar / 7.37) * 1000
        m_solar = P_solar / 275
        t = params["flightRange"] / params["velocity"]
        params["solarPower"] = P_solar
        params["solarEnergy"] = P_solar * t
        print(f"Solar energy: {params['solarEnergy']} J")
        params["solarMass"] = m_solar
    else:
        params["solarPower"] = 0
        params["solarMass"] = 0
        params["solarEnergy"] = 0
