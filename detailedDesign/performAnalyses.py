import logging
import matplotlib.pyplot as plt

from detailedDesign.analysis.marketEstimations import market_estimations
from detailedDesign.analysis.find_stability import find_stability
from detailedDesign.sketch import sketch_aircraft

logger = logging.getLogger("logger")


def perform_analyses(aircraft):
    # sketch_aircraft(aircraft)
    print_summary(aircraft)
    # find_stability(aircraft)
    price_ac, cost_per_passenger_km, cost_breakdown, breakdown_summary = market_estimations(aircraft)
    print(f"Aircraft CG: {aircraft.get_cg()}")
    print(f"Cost breakdown summary: {breakdown_summary}")
    print(f"Aircraft Price [M$]: {price_ac / 1e6:.2f}")
    print(f"Direct Operating Cost / ASK [$/pax/km]: {cost_per_passenger_km:.4f}")
    plt.show()


def print_summary(aircraft):
    logger.debug(
        f"MTOM = {aircraft.mtom:.4E} kg, OEM = {aircraft.oem:.4E} kg, Fuel Mass = {aircraft.fuel_mass:.4E}")
    logger.debug(f"{aircraft.cruise_drag = :.4E} N")
    logger.debug(f"Wing Area: {aircraft.reference_area:.2f} m2")

    engines = aircraft.WingGroup.Engines
    logger.debug(f"Amount of propellors: {engines.own_amount_prop} [-]")
    logger.debug(f"Amoung of motors: {engines.own_amount_motor} [-]")
    logger.debug(f"Unit dimensions (L x W x H) ({engines.own_lenght_unit:.3f} x {engines.own_width_unit:.3f} x {engines.own_height_unit:.3f}) [m]")
    logger.debug(f"Clean stall speed : {aircraft.clean_stall_speed} m/s")
    logger.debug(f"W/S : {aircraft.weight_over_surface} N/m2")

    logger.debug(f"Wing Span: {aircraft.WingGroup.Wing.span} m")

    logger.debug(f"Fuselage Length: {aircraft.FuselageGroup.Fuselage.length} m")
    logger.debug(f"H Tail Length: {aircraft.FuselageGroup.Tail.VerticalTail.tail_length} m")
    logger.debug(f"V Tail Length: {aircraft.FuselageGroup.Tail.HorizontalTail.tail_length} m")

    cabin = aircraft.FuselageGroup.Fuselage.Cabin
    logger.debug(f"{ cabin.length = } {cabin.width = } {cabin.height = }")

    logger.debug(f"{aircraft.FuselageGroup.Power.FuelCells.size = }")
