import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from functools import reduce
from misc.unitConversions import *
from tabulate import tabulate

# Personnel constants
salaryMaintenance = 50  # [$/h]
crewCount = 5  # [-]
annualAttendantSalary = 85e3  # [$]
annualPilotSalary = 175e3  # [$]
# TODO: check this number and unit for cost burden
costBurden = 2  # [$]

# Operational constants
h2_price = 1.9  # [$/kg] as suggested by hydrogen experts
maintenance_time = 2749  # [h]
block_time_supplement = 1.8  # [h]
f_atc = 0.7  # [-] 0.7 as ATC fees for transatlantic

# CAPEX constants
P_OEW = 1200 * 1.5  # [$/kg] operating empty weight
P_eng = 2600  # [$/kg] engine
P_fc = 608  # [$/kg] fuel cell --> 320 [$/kg] for 2025 estimate
P_tank = 550  # [$/kg] LH2

IR = 0.05  # 5% Interest rate
f_rv = 0.1  # 10% Residual value factor
f_ins = 0.005  # 0.5% insurance cost
f_misc = 0.1  # Misc 5% contingency factor to account for new tech
PMac = 0.2  # typically 20% profit margin for manufacturer
DP = 14  # Depreciation period [yrs], could do 27 as well

# Return on investment constants
price_per_ticket = 600  # Average price today
# price_per_ticket = 935.80  # Adjusted for inflation expectation in 2040
price_per_cargo = 6  # [$/kg]
subsidy = 0.  # expected subsidy for green aviation
n_ac_sold = 119  # TODO: Revise this w market analysis


def operations_and_logistics(aircraft):
    # ----- Calculating ground time ----- [h]  --> refuelling (depends on fuel) + boarding payload

    # Initialise
    n_doors = 8  # [-]
    refuelling_rate = 35500  # [kg/h]
    n_pumps = 3  # [-]
    loading_bags = 1.2 / 60  # [h/container]
    unloading_bags = 1.2 / 60  # [h/container]
    boarding = 18 * 60 * n_doors  # [pax/h]
    deboarding = 28 * 60 * n_doors  # [pax/h]
    n_pax = aircraft.FuselageGroup.Fuselage.Cabin.passenger_count
    bag_containers = np.ceil(n_pax / 30)

    # Refuelling
    refuelling_time = aircraft.fuel_mass / (refuelling_rate * n_pumps)

    # Cargo
    loading_bag_time = bag_containers * loading_bags
    unloading_bag_time = bag_containers * unloading_bags
    cargo_time = loading_bag_time + unloading_bag_time

    # Cabin
    cleaning_time = 25 / 60  # [h]
    catering_time = 20 / 60  # [h]
    boarding_time = n_pax / boarding
    deboarding_time = n_pax / deboarding
    last_pax_delay = 4 / 60  # [h]
    cabin_time = cleaning_time + catering_time + boarding_time \
                 + deboarding_time + last_pax_delay

    print(f"{boarding_time = }")
    print(f"{deboarding_time = }")
    print(f"{refuelling_time = }")
    print(f"{cargo_time = }")
    print(f"{cabin_time = }")

    return max(refuelling_time, cargo_time, cabin_time)


def production_cost_estimation(aircraft):
    oew = aircraft.oew  # [kg]
    state = aircraft.states['cruise']
    n_pax = aircraft.FuselageGroup.Fuselage.Cabin.passenger_count
    flight_range = state.range  # [m]

    # ----- Estimating competitive price of the aircraft -----
    # Wide body aircraft reference data
    k1 = 0.508
    k2 = 0.697
    alpha = 2.760
    seats_ref = 853  # [A380 reference]
    range_ref = 15200  # [km - A380 reference]
    price_ac_ref = int(450e6)  # [$ - A380 reference]

    competitive_price_ac = (k1 * (n_pax / seats_ref) ** alpha + k2 * (flight_range / (1e3 * range_ref))) * price_ac_ref

    # ----- Non-Recurring Costs -----
    engineering_cost = 0.4
    me_cost = 0.1
    tool_design_cost = 0.15
    tool_fab_cost = 0.348
    support_cost = 0.047

    wing_mass = aircraft.WingGroup.Wing.own_mass
    empennage_mass = aircraft.FuselageGroup.Tail.total_mass
    fuselage_mass = aircraft.FuselageGroup.Fuselage.own_mass
    engine_mass = aircraft.WingGroup.Engines.own_mass
    miscellaneous_mass = aircraft.FuselageGroup.Miscellaneous.own_mass

    # Cost density [$/lb]
    wing_cost_density = 17731
    empennage_cost_density = 52156
    fuselage_cost_density = 32093
    engine_cost_density = 8691
    miscellaneous_cost_density = 34307

    wing_mass_usd = wing_cost_density * kg_to_lbs(wing_mass)
    empennage_mass_usd = empennage_cost_density * kg_to_lbs(empennage_mass)
    fuselage_mass_usd = fuselage_cost_density * kg_to_lbs(fuselage_mass)
    engine_mass_usd = engine_cost_density * kg_to_lbs(engine_mass)
    miscellaneous_mass_usd = miscellaneous_cost_density * kg_to_lbs(miscellaneous_mass)

    lst_1 = [engineering_cost, me_cost, tool_design_cost, tool_fab_cost,
             support_cost, 1]
    lst_2 = [wing_mass_usd, empennage_mass_usd, fuselage_mass_usd, engine_mass_usd, miscellaneous_mass_usd]
    lst_2.append(sum(lst_2))
    lst_3 = ['Wing', 'Empennage', 'Fuselage', 'Engines', 'Miscellaneous',
             'aircraft total']
    columns = ['Engineering', 'ME', 'Tool Design', 'Tool Fab', 'Support',
               'Totals']
    nrc_per_kg = np.array([[item_3] + [(item_1 * item_2) / 1e6 for item_1 in lst_1] for
                           item_2, item_3 in zip(lst_2, lst_3)])

    print()
    print("-----------NON RECURRING COSTS-----------")
    print()
    print(tabulate(nrc_per_kg, headers=columns, floatfmt=".2f"))
    print()
    print()

    total_nrc = float(nrc_per_kg[-1, -1])

    # ----- Recurring Costs ----- [per aircraft]

    # Cost density [$/lb]
    wing_rec_cost_density = 900
    empennage_rec_cost_density = 2331
    fuselage_rec_cost_density = 967
    # TODO: Revise engine cost from Saluqi
    engine_rec_cost_density = 374
    miscellaneous_rec_cost_density = 452
    final_assembly_rec_cost_density = 65

    wing_rec_mass_usd = wing_rec_cost_density * kg_to_lbs(wing_mass)
    empennage_rec_mass_usd = empennage_rec_cost_density * kg_to_lbs(empennage_mass)
    fuselage_rec_mass_usd = fuselage_rec_cost_density * kg_to_lbs(fuselage_mass)
    engine_rec_mass_usd = engine_rec_cost_density * kg_to_lbs(engine_mass)
    # engine_rec_mass_usd = P_eng * engine_mass
    fuel_cell_rec_mass_usd = P_fc * aircraft.FuselageGroup.Power.FuelCells.own_mass
    fuel_tank_rec_mass_usd = P_tank * aircraft.FuselageGroup.Fuselage.fuel_tank_mass
    miscellaneous_rec_mass_usd = miscellaneous_rec_cost_density * kg_to_lbs(miscellaneous_mass)
    final_assembly_rec_mass_usd = final_assembly_rec_cost_density * kg_to_lbs(oew)

    total_rc_per_ac = wing_rec_mass_usd + empennage_rec_mass_usd + fuselage_rec_mass_usd + engine_rec_mass_usd + fuel_cell_rec_mass_usd + fuel_tank_rec_mass_usd + miscellaneous_rec_mass_usd + final_assembly_rec_mass_usd

    total_program_cost = (total_rc_per_ac * n_ac_sold) / 1e6 + total_nrc

    non_rec_costs_totals = [float(i[-1]) for i in nrc_per_kg[:-1]]
    colors = [plt.cm.Pastel1(i) for i in range(20)]
    plt.clf()
    plt.pie(non_rec_costs_totals, labels=lst_3[:-1], autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title("Non Recurring Cost Breakdown [%]")
    plt.axis('equal')

    plt.savefig(Path("plots", "non_recurring_market_pie.png"))

    rec_costs_totals = [wing_rec_mass_usd, empennage_rec_mass_usd,
                        fuselage_rec_mass_usd, engine_rec_mass_usd,
                        fuel_cell_rec_mass_usd, fuel_tank_rec_mass_usd,
                        miscellaneous_rec_mass_usd, final_assembly_rec_mass_usd]
    rec_costs_totals.append(sum(rec_costs_totals))
    rec_costs_totals = np.array(rec_costs_totals)

    rec_cost_labels = ['Wing', 'Empennage', 'Fuselage', 'Engines', 'Fuel Cells', 'Fuel Tank',
                       'Miscellaneous', 'Final Assembly', 'Total']

    print()
    print("-----------RECURRING COSTS-----------")
    print()
    print(tabulate(rec_costs_totals.reshape(1, len(rec_costs_totals)) / 1e6, headers=rec_cost_labels, floatfmt=".2f"))
    print()
    print()

    plt.clf()
    plt.pie(rec_costs_totals[:-1], labels=rec_cost_labels[:-1], autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title("Recurring Cost Breakdown [%]")
    plt.axis('equal')
    plt.savefig(Path("plots", "recurring_market_pie.png"))

    # Return on investment
    price_ac = (total_rc_per_ac + total_nrc / n_ac_sold) * (1 + PMac + f_misc)
    program_revenues = n_ac_sold * price_ac / 1e6
    program_roi = (program_revenues - total_program_cost) / total_program_cost * 100

    return competitive_price_ac, total_program_cost, program_roi, total_rc_per_ac / 1e6, total_nrc


def market_estimations(aircraft, total_rc_per_ac, total_nrc, ground_time):
    # Initialise
    state = aircraft.states['cruise']
    n_pax = aircraft.FuselageGroup.Fuselage.Cabin.passenger_count
    n_motor = aircraft.WingGroup.Engines.own_amount_fans
    flight_range = state.range  # [m]
    block_time = state.duration / 3600 + block_time_supplement  # [h]
    mtow = aircraft.mtom  # [kg]
    fuel_mass = aircraft.fuel_mass  # [kg]
    oew = aircraft.oew  # [kg]
    payload = aircraft.get_payload_mass  # [kg]

    # Calculate yearly flight cycles
    year_time = 365.242199 * 24  # [h]
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
    ton_force = aircraft.reference_cruise_thrust * 0.0001124
    DOC_maint_engine = n_motor * (1.5 * ton_force + 30.5 * block_time + 10.6)
    DOC_maintenance = flight_cycles * (DOC_maint_engine + DOC_maint_material + DOC_maint_personnel)  # [$]

    # DOC capex (engines, fuel cell, fuel tak, cont. factor incl)
    a = IR * (1 - f_rv * (1 / (1 + IR)) ** DP) / (1 - (1 / (1 + IR)) ** DP)

    price_ac = (total_rc_per_ac + total_nrc / n_ac_sold) * (1 + PMac + f_misc) * 1e6
    DOC_cap = price_ac * (a + f_ins)

    DOC = DOC_maintenance + DOC_crew + DOC_fees + DOC_fuel + DOC_cap  # [$]
    available_seat_km = flight_cycles * flight_range * n_pax / 1000
    cost_per_passenger_km = DOC / available_seat_km  # [$/km/passenger]

    # Cost Breakdown [%]
    frac_maintenance = DOC_maintenance / DOC * 100
    frac_crew = DOC_crew / DOC * 100
    frac_fees = DOC_fees / DOC * 100
    frac_fuel = DOC_fuel / DOC * 100
    frac_cap = DOC_cap / DOC * 100

    cost_breakdown = [
        {"cost type": "Maintenance", "fraction": frac_maintenance},
        {"cost type": "Crew", "fraction": frac_crew},
        {"cost type": "Fees", "fraction": frac_fees},
        {"cost type": "Fuel", "fraction": frac_fuel},
        {"cost type": "CAPEX", "fraction": frac_cap}
    ]

    cost_type = list(map(lambda x: x['cost type'], cost_breakdown))
    cost_fraction = list(map(lambda x: x['fraction'], cost_breakdown))

    breakdown_summary = reduce(
        lambda out_str, cost_item: f"{out_str}\n  {cost_item['cost type']} : {cost_item['fraction']:.2f} %",
        cost_breakdown, 'Cost breakdown summary:')

    # Plotting pie chart
    colors = [plt.cm.Pastel1(i) for i in range(20)]
    plt.clf()
    plt.pie(cost_fraction, labels=cost_type, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title("Operational Cost Breakdown [%]")
    plt.axis('equal')
    # costBreakdownPath = Path("plots","costBreakdown")
    plt.savefig(Path("plots", "operational_market_pie.png"))

    # Calculating ROI
    revenue_per_flight = price_per_ticket * n_pax * (1 + subsidy) + price_per_cargo * aircraft.cargo_mass
    cost_per_flight = DOC / flight_cycles
    roi = (revenue_per_flight - cost_per_flight) / cost_per_flight * 100  # [%]

    return price_ac, cost_per_passenger_km, cost_breakdown, breakdown_summary, roi
