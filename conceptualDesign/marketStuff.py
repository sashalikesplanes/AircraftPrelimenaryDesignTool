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

    # DOC fees
    DOC_fees = flightCycles * (h2Price * fuelMass + payload * 0.1 + 0.01 * MTOW + 0.7 * flightRange / 1000 * (MTOW/5e4) ** 0.5 + 541)

    # DOC crew
    countAttendant = np.ceil(params["passengers"] / 50)  # [-]
    countPilot = params["pilotCount"]  # [-]
    crewCount = 5
    annualAttendantSalary = 85e3
    annualPilotSalary = 175e3
    DOC_crew = crewCount * (countAttendant * annualAttendantSalary + countPilot * annualPilotSalary)

    # DOC maintenance
    DOC_maint_material = OEW / 1e3 * (0.21 * blockTime + 13.7) + 57.5
    DOC_maint_personnel = salaryMaintenance * (1 + costBurden) * ((0.655 + 0.01 * OEW / 1e3) * blockTime + 0.254 + OEW / 1e5)
    tonForce = params["engineThrust"] * 0.0001124
    DOC_maint_engine = params["engineCount"] * (1.5 * tonForce + 30.5 * blockTime + 10.6)
    DOC_maintenance = DOC_maint_engine + DOC_maint_material + DOC_maint_personnel  # [$]

    # DOC capex
    # # IR = 0.05
    # # f_rv = 0.05
    # # f_ins = 0.005
    # # f_misc = 0.05  # TODO: Unknown correctness
    # # DP = 14
    # # a = IR * (1-f_rv * (1/(1+IR)) ** DP)/(1-(1/(1+IR)) ** DP)
    # # TODO: finish capex stuff
    DOC_cap = 406.5e6  # [$]

    DOC = DOC_maintenance + DOC_crew + DOC_fees + DOC_cap  # [$]
    availableSeatKM = flightCycles * flightRange * params["passengers"] / 1000
    params["costPerPassengerKilometer"] = DOC/availableSeatKM  # [$/km/passenger]


if __name__ == "__main__":
    x = {
        "totalMass": 171e3,
        "fuelMass": 31.2e3,
        "velocity": 273,
        "flightRange": 7408e3,
        "payloadMass": 150000,
        "pilotCount": 2,
        "passengers": 290*120,
        "engineCount": 2,
        "engineThrust": 3.6e5
    }

    marketStuff(x)
