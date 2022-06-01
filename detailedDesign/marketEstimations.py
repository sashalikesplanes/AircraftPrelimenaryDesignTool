import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from detailedDesign.classes.State import State
from misc.constants import *

# Personnel constants
salaryPilot = 69  # [$/h]
salaryAttendant = 38  # [$/h]
salaryMaintenance = 50  # [$/h]
crewCount = 5  # [-]
annualAttendantSalary = 85e3  # [$]
annualPilotSalary = 175e3  # [$]
# TODO: check this number and unit for cost burden
costBurden = 2  # [$]

# Operational constants
h2_price = 2.5  # [$/kg]
ground_time = 10  # [h]  --> refuelling (depends on fuel) + boarding payload
maintenance_time = 2749  # [h]
block_time_supplement = 1.8  # [h]
f_atc = 0.7  # [-] 0.7 as ATC fees for transatlantic

# CAPEX constants

# TODO: Revise CAPEX calculations to incorporate fuel tank costs properly
P_OEW = 1200  # [$/kg] operating empty weight
W_eng = 200  # Weight per engine [kg]
P_eng = 2600  # [$/kg] engine
P_fc = 608  # [$/kg] fuel cell
P_tank = 550  # [$/kg] LH2

IR = 0.05  # 5% Interest rate
f_rv = 0.1  # 10% Residual value factor
f_ins = 0.005  # 0.5% insurance cost
f_misc = 0.05  # Misc 5% contingency factor to account for new tech
PMac = 0.0  # typically 20% profit margin for manufacturer
DP = 14  # Depreciation period [yrs]


def marketStuff(aircraft):
    # Initialise
    state = aircraft.states['cruise']
    n_pax = aircraft.FuselageGroup.Fuselage.Cabin.passengers
    n_motor = aircraft.WingGroup.Engines.own_amount_motor

    flight_range = state.range  # [m]
    block_time = state.duration / 3600 + block_time_supplement  # [h]
    mtow = aircraft.mtom  # [kg]
    fuel_mass = aircraft.fuel_mass  # [kg]
    oew = aircraft.oew  # [kg]
    payload = aircraft.get_payload_mass()  # [kg]

    # Calculate yearly flight cycles
    year_time = 365 * 24  # [h]
    operational_time = year_time - maintenance_time  # [h]
    flight_cycles = operational_time / (block_time + ground_time)  # [-]

    # DOC fuel for a year
    DOC_fuel = flight_cycles * h2_price * fuel_mass

    # DOC fees for a year (payload handling, landing, atc)
    DOC_fees = flight_cycles * (payload * 0.1 + 0.01 * mtow + f_atc * flight_range / 1000 * (mtow / 50 / 1000) ** 0.5)

    # DOC crew

    count_attendant = np.ceil(n_pax / 50)  # [-]
    count_pilot = aircraft.count_pilot  # [-]

    DOC_crew = crewCount * (count_attendant * annualAttendantSalary + count_pilot * annualPilotSalary)

    # DOC maintenance
    DOC_maint_material = oew / 1000 * (0.21 * block_time + 13.7) + 57.5
    DOC_maint_personnel = salaryMaintenance * (1 + costBurden) * (
            (0.655 + 0.01 * oew / 1000) * block_time + 0.254 + 0.01 * oew / 1000)
    ton_force = aircraft.reference_thrust * 0.0001124
    DOC_maint_engine = n_motor * (1.5 * ton_force + 30.5 * block_time + 10.6)
    DOC_maintenance = flight_cycles * (DOC_maint_engine + DOC_maint_material + DOC_maint_personnel)  # [$]

    # DOC capex (engines, fuel cell, fuel tak, cont. factor incl)
    # TODO: Revise price_ac calc. Should the other masses be subtracted from oew?
    a = IR * (1 - f_rv * (1 / (1 + IR)) ** DP) / (1 - (1 / (1 + IR)) ** DP)
    # price_ac = (P_OEW * (oew - W_eng * params["engineCount"]) + W_eng * params["engineCount"] * P_eng + params[
    # "balloonStructuralMass"] * P_tank + params["fuelCellMass"] * P_fc) * (1 + PMac + f_misc)

    price_ac = (P_OEW * (oew - W_eng * n_motor - aircraft.FuselageGroup.Fuselage.FuelContainer.own_mass
                         - aircraft.FuselageGroup.Power.FuelCells.own_mass) + W_eng * n_motor * P_eng
                + aircraft.FuselageGroup.Fuselage.FuelContainer.own_mass * P_tank
                + aircraft.FuselageGroup.Power.FuelCells.own_mass * P_fc) * (1 + PMac + f_misc)

    DOC_cap = price_ac * (a + f_ins)

    # print(price_ac)

    DOC = DOC_maintenance + DOC_crew + DOC_fees + DOC_fuel + DOC_cap  # [$]
    available_seat_km = flight_cycles * flight_range * n_pax / 1000
    cost_per_passenger_km = DOC / available_seat_km  # [$/km/passenger]

    # Cost Breakdown [%]
    frac_maintenance = DOC_maintenance / DOC * 100
    frac_crew = DOC_crew / DOC * 100
    frac_fees = DOC_fees / DOC * 100
    frac_fuel = DOC_fuel / DOC * 100
    frac_cap = DOC_cap / DOC * 100

    # print(f"Aircraft Price [$]: {price_ac}")
    # print(f"Direct Operating Cost / ASK [$/pax/km]: {params['costPerPassengerKilometer']}")
    # print(f"Cost breakdown [%]: {frac_maintenance}, {frac_crew}, {frac_fees }, { frac_fuel}, {frac_cap}")

    # # Make pie chart
    # breakdown = np.array([frac_maintenance, frac_crew, frac_fees, frac_fuel, frac_cap])
    # mylabels = ["Maintenance", "Crew", "Fees", "Fuel", "CAPEX"]
    # colors = [plt.cm.Pastel1(i) for i in range(20)]
    # plt.pie(breakdown, labels=mylabels, autopct='%1.1f%%', colors=colors, startangle=90)
    # plt.title("Cost Breakdown [%]")
    # plt.axis('equal')
    # costBreakdownPath = Path("plots","costBreakdown")
    # plt.savefig(costBreakdownPath, dpi = 600)
    # # plt.show()

    return cost_per_passenger_km