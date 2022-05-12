import numpy as np


salaryPilot = 69  # [$/h]
salaryAttendant = 38  # [$/h]
salaryMaintenance = 50  # [$/h]
# TODO: check this number and unit for cost burden
costBurden = 2  # [$]

h2Price = 2.5  # [$/kg]
groundTime = 4  # [h]  --> refuelling (depends on fuel) + boarding payload
maintenanceTime = 2749  # [h]
blockTimeSupplement = 1.8  # [h]
f_atc = 0.5  # [-]


def marketStuff(params):
    # Calculate block time
    flightRange = params["flightRange"]  # [m]
    MTOW = params["totalMass"]  # [kg]
    fuelMass = params["fuelMass"]  # [kg]
    flightTime = flightRange/params["velocity"]/3600  # [h]
    blockTime = flightTime + blockTimeSupplement  # [h]
    OEW = (MTOW - fuelMass - params["payloadMass"])  # [kg]
    payload = params["payloadMass"]

    # Calculate yearly flight cycles
    yearTime = 365 * 24  # [h]
    operationalTime = yearTime - maintenanceTime  # [h]
    flightCycles = operationalTime / (blockTime + groundTime)  # [-]

    # # DOC energy
    # DOC_energy = flightCycles * fuelMass * h2Price  # [$]
    #
    # # DOC fees
    # DOC_handling = 0.1 * params["payloadMass"]  # [$]
    # DOC_landing = 0.01 * MTOW  # [$]
    # DOC_atc = f_atc * flightRange * (MTOW / 50000) ** 0.5  # [$]
    # # TODO: decide if we multiply by flight cycles
    DOC_fees = flightCycles * (h2Price * fuelMass + payload * 0.1 + 0.01 * MTOW + 0.7 * flightRange / 1000 * (MTOW/5e4) ** 0.5 + 541)





    # DOC_fees = (DOC_handling + DOC_landing + DOC_atc) * flightCycles  # [$]

    # DOC crew
    countAttendant = np.ceil(params["passengers"] / 50)  # [-]
    countPilot = params["pilotCount"]  # [-]
    # hourlyCrewPrice = (countAttendant * salaryAttendant + countPilot * salaryPilot)  # [$/h]
    # DOC_crew = hourlyCrewPrice * flightCycles * blockTime  # [$]
    crewCount = 5
    annualAttendantSalary = 85e3
    annualPilotSalary = 175e3
    DOC_crew = crewCount * (countAttendant * annualAttendantSalary + countPilot * annualPilotSalary)
    #
    # print(DOC_crew1, DOC_crew2)
    # # DOC maintenance
    DOC_maint_material = OEW / 1e3 * (0.21 * blockTime + 13.7) + 57.5
    DOC_maint_personnel = salaryMaintenance * (1 + costBurden) * ((0.655 + 0.01 * OEW / 1e3) * blockTime + 0.254 + OEW / 1e5)
    tonForce = params["engineThrust"] * 0.0001124
    DOC_maint_engine = params["engineCount"] * (1.5 * tonForce + 30.5 * blockTime + 10.6)
    DOC_maintenance = DOC_maint_engine + DOC_maint_material + DOC_maint_personnel  # [$]
    #
    # # DOC capex
    # # IR = 0.05
    # # f_rv = 0.05
    # # f_ins = 0.005
    # # f_misc = 0.05  # TODO: Unknown correctness
    # # DP = 14
    # # a = IR * (1-f_rv * (1/(1+IR)) ** DP)/(1-(1/(1+IR)) ** DP)
    # # TODO: finish capex stuff
    DOC_cap = 406.5e6  # [$]
    #
    # # Final DOC
    # # TODO: check which things are multiplied by flight cycles

    DOC = DOC_maintenance + DOC_crew + DOC_fees + DOC_cap  # [$]
    availableSeatKM = flightCycles * flightRange * params["passengers"] / 1000
    print(DOC)
    print(f"Price per km per passenger: {DOC/availableSeatKM}")  # [$/km/passenger]
    ticketPrice = DOC/availableSeatKM * flightRange / 1000
    print(f"Ticket price: {ticketPrice}")


if __name__ == "__main__":
    x = {
        "totalMass": 447.7e3,
        "fuelMass": 2e5,
        "velocity": 933/3.6,
        "flightRange": 1e7,
        "payloadMass": 150000,
        "pilotCount": 3,
        "passengers": 500,
        "engineCount": 4,
        "engineThrust": 300e3
    }

    marketStuff(x)