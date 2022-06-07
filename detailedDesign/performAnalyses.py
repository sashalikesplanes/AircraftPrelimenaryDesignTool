import logging
import matplotlib.pyplot as plt

from detailedDesign.analysis.marketEstimations import market_estimations, production_cost_estimation
from detailedDesign.analysis.find_stability import find_stability
from detailedDesign.sketch import sketch_aircraft
from detailedDesign.analysis.make_avl_file import make_avl_file

logger = logging.getLogger("logger")


def perform_analyses(aircraft, make_stability):
    make_avl_file(aircraft)
    sketch_aircraft(aircraft)
    print_summary(aircraft)
    plt.figure(2)

    if make_stability:
        find_stability(aircraft)
        plt.figure(3)

    competitive_price_ac, cost_ac, cost_per_passenger_km, cost_breakdown, breakdown_summary, roi = market_estimations(aircraft)
    total_program_cost = production_cost_estimation(aircraft)
    print(f"Aircraft CG: {aircraft.get_cg()}")
    print(f"{breakdown_summary}")
    print(f"Aircraft Cost [M$]: {cost_ac / 1e6:.2f}")
    print(f"Competitive Aircraft Price [M$]: {competitive_price_ac / 1e6:.2f}")
    print(f"Direct Operating Cost / ASK [$/pax/km]: {cost_per_passenger_km:.4f}")
    print(f"Total Program Cost [M$]: {total_program_cost :.2f}")
    plt.show()


def print_summary(aircraft):
    logger.debug(
        f"MTOM = {aircraft.mtom:.4E} kg, OEM = {aircraft.oem:.4E} kg, Fuel Mass = {aircraft.fuel_mass:.4E}")
    logger.debug(f"{aircraft.cruise_drag = :.4E} N")
    logger.debug(f"Wing Area: {aircraft.reference_area:.2f} m2")

    fuselage = aircraft.FuselageGroup.Fuselage
    logger.debug(f"Ass length: {fuselage.AssFuelContainer.length} m")
    logger.debug(f"Fuselage Length: {fuselage.length} m")
    logger.debug(f"Forward fuel length: {fuselage.ForwardFuelContainer.length} m")
    logger.debug(f"Aft fuel length: {fuselage.AftFuelContainer.length} m")

    engines = aircraft.WingGroup.Engines
    # logger.debug(f"Amount of propellors: {engines.own_amount_prop} [-]")
    # logger.debug(f"Amoung of motors: {engines.own_amount_motor} [-]")
    # logger.debug(f"Unit dimensions (L x W x H) ({engines.own_lenght_unit:.3f} x {engines.own_width_unit:.3f} x {engines.own_height_unit:.3f}) [m]")
    # logger.debug(f"Clean stall speed : {aircraft.clean_stall_speed} m/s")
    # logger.debug(f"W/S : {aircraft.weight_over_surface} N/m2")

    logger.debug(f"Wing Span: {aircraft.WingGroup.Wing.span} m")

    logger.debug(f"Fuselage Length: {aircraft.FuselageGroup.Fuselage.length} m")
    logger.debug(f"V Tail Length: {aircraft.FuselageGroup.Tail.VerticalTail.tail_length} m")
    logger.debug(f"H Tail Length: {aircraft.FuselageGroup.Tail.HorizontalTail.tail_length} m")
    logger.debug(f"V Tail area: {aircraft.FuselageGroup.Tail.VerticalTail.surface_area} m2") 

    cabin = aircraft.FuselageGroup.Fuselage.Cabin
    logger.debug(f"{ cabin.length = } {cabin.width = } {cabin.height = }")

    logger.debug(f"{aircraft.FuselageGroup.Power.FuelCells.size = }")

    engines = aircraft.WingGroup.Engines
    logger.debug(f"Wing span: {aircraft.WingGroup.Wing.span} m")
    logger.debug(f"Diameter fans: {engines.own_diameter_fan}")
    logger.debug(f"N fans on wing: {engines.own_fans_on_wing}")
    logger.debug(f"N fans on fus: {engines.own_fans_on_fuselage}")

