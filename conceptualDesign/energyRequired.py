def energyRequired(params):
    E_req = params["totalDrag"] * \
        params["flightRange"] / params["propEfficiency"]
    params["requiredEnergy"] = E_req

    if params["hasSolarPanels"]:
        S_solar = params["balloonLength"] * params["balloonRadius"]

        # Using HES flexible array
        # print(f"Solar area: {S_solar} m^2")
        # Calculate power generated and mass for solar panels
        # TODO: remove hard coding of these values
        P_solar = (S_solar / 3.12) * 1000
        m_solar = P_solar / 70

        # Caclulate flight time to calculate energy
        t = params["flightRange"] / params["velocity"]
        params["solarEnergy"] = P_solar * t

        # Save outputs to params
        params["solarPower"] = P_solar
        # print(f"Solar energy: {params['solarEnergy']} J")
        params["solarMass"] = m_solar
    else:
        params["solarPower"] = 0
        params["solarMass"] = 0
        params["solarEnergy"] = 0
