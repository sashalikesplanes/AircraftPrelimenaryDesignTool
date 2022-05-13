import numpy as np

# Personnel constants
salaryPilot = 69  # [$/h]
salaryAttendant = 38  # [$/h]
salaryMaintenance = 50  # [$/h]
crewCount = 5   # [-]
annualAttendantSalary = 85e3   # [$]
annualPilotSalary = 175e3       # [$]
# TODO: check this number and unit for cost burden
costBurden = 2  # [$]

# Operational constants
h2Price = 2.5  # [$/kg]
groundTime = 4  # [h]  --> refuelling (depends on fuel) + boarding payload
maintenanceTime = 2749  # [h]
blockTimeSupplement = 1.8  # [h]
f_atc = 0.7  # [-] 0.7 as ATC fees for transatlantic

# CAPEX constants
AircraftCost = 800e6    # [$] - should be changed

# TODO: Revise CAPEX calculations to incorporate fuel tank costs properly
# TODO: Do cost calculation for GH2 vs LH2
P_OEW = 1200    # Price per operating empty weight [$/kg]
P_eng = 2500    # price per engine weight
W_eng = 2000
IR = 0.05
f_rv = 0.1
f_ins = 0.005
f_misc = 0.05  # TODO: Unknown correctness
DP = 14


def marketStuff(params):
    # Calculate block time
    flightRange = params["flightRange"]  # [m]
    MTOW = params["totalMass"]  # [kg]
    fuelMass = params["fuelMass"]  # [kg]
    flightTime = flightRange / params["velocity"] / 3600  # [h]
    blockTime = flightTime + blockTimeSupplement  # [h]
    OEW = (MTOW - fuelMass - params["payloadMass"])  # [kg]
    payload = params["payloadMass"]

    # Calculate yearly flight cycles
    yearTime = 365 * 24  # [h]
    operationalTime = yearTime - maintenanceTime  # [h]
    flightCycles = operationalTime / (blockTime + groundTime)  # [-]

    # DOC fuel for a year
    DOC_fuel = flightCycles * h2Price * fuelMass

    # DOC fees for a year (payload handling, landing, atc)
    DOC_fees = flightCycles * (payload * 0.1 + 0.01 * MTOW + f_atc * flightRange / 1000 * (MTOW / 50 / 1000) ** 0.5)

    # DOC crew
    countAttendant = np.ceil(params["passengers"] / 50)  # [-]
    countPilot = params["pilotCount"]  # [-]
    DOC_crew = crewCount * (countAttendant * annualAttendantSalary + countPilot * annualPilotSalary)

    # DOC maintenance
    DOC_maint_material = OEW / 1000 * (0.21 * blockTime + 13.7) + 57.5
    DOC_maint_personnel = salaryMaintenance * (1 + costBurden) * (
                (0.655 + 0.01 * OEW / 1000) * blockTime + 0.254 + 0.01 * OEW / 1000)
    tonForce = params["engineThrust"] * 0.0001124
    DOC_maint_engine = params["engineCount"] * (1.5 * tonForce + 30.5 * blockTime + 10.6)
    DOC_maintenance = flightCycles * (DOC_maint_engine + DOC_maint_material + DOC_maint_personnel)  # [$]

    # DOC capex
    a = IR * (1-f_rv * (1/(1+IR)) ** DP)/(1-(1/(1+IR)) ** DP)
    DOC_cap = (P_OEW * (OEW - W_eng*params["engineCount"])+W_eng*params["engineCount"]*P_eng)*(a+f_ins)


    # # TODO: finish capex stuff
    # DOC_cap = AircraftCost  # [$]



    DOC = DOC_maintenance + DOC_crew + DOC_fees + DOC_fuel + DOC_cap  # [$]
    availableSeatKM = flightCycles * flightRange * params["passengers"] / 1000
    params["costPerPassengerKilometer"] = DOC / availableSeatKM  # [$/km/passenger]

    # Cost Breakdown [%]
    frac_maintenance = DOC_maintenance / DOC
    frac_crew = DOC_crew / DOC
    frac_fees = DOC_fees / DOC
    frac_fuel = DOC_fuel / DOC
    frac_cap = DOC_cap / DOC
    print(params["costPerPassengerKilometer"])
    print(frac_maintenance, frac_crew, frac_fees, frac_fuel, frac_cap)


if __name__ == "__main__":
    x = {
        "totalMass": 800e3,
        "fuelMass": 82e3,
        "velocity": 200,
        "flightRange": 8000e3,  # m
        "payloadMass": 120000,
        "pilotCount": 2,
        "passengers": 1000,
        "engineCount": 86,
        "engineThrust": 6600  # power / velocity
    }

    marketStuff(x)
