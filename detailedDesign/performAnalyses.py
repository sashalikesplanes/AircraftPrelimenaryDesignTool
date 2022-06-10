import logging
import matplotlib.pyplot as plt

from detailedDesign.analysis.marketEstimations import market_estimations, production_cost_estimation, operations_and_logistics
from detailedDesign.analysis.find_stability import find_stability
from detailedDesign.sketch import sketch_aircraft
from detailedDesign.analysis.make_avl_file import make_avl_file
from detailedDesign.analysis.make_payload_range_diagram import make_payload_range_diagram
from detailedDesign.analysis.loading_diagrams import make_loading_diagrams
from detailedDesign.climbPerformance import get_max_climb_rate, get_climb_angle, get_power_plot, calc_ROC
from detailedDesign.potatoPlot import make_potato_plot
import numpy as np
from misc.constants import g

logger = logging.getLogger("logger")


def perform_analyses(aircraft, make_stability):
    # make_avl_file(aircraft)
    # 
    # plt.figure()
    # sketch_aircraft(aircraft)
    print_summary(aircraft)
    # make_payload_range_diagram(aircraft)
    get_power_plot(aircraft)
    # make_potato_plot(aircraft, True)
    logger.debug(f"Max climb rate obtained at a velocity of {get_max_climb_rate(aircraft)[1]} m/s\n"
                 f"Max climb rate : {get_max_climb_rate(aircraft)[0]}m/s")
    logger.debug(f'climb angle the plane can fly at cruise: {get_climb_angle(aircraft)} degrees')
    logger.debug(f"ROC @ TO speed of {aircraft.takeoff_speed} m/s:{calc_ROC(aircraft, True, aircraft.takeoff_speed)}m/s")

    plt.figure()
    if make_stability:
        find_stability(aircraft)
        plt.figure()

    ground_time = operations_and_logistics(aircraft)
    competitive_price_ac, total_program_cost, program_roi, average_price, total_nrc, breakeven_point = production_cost_estimation(aircraft)
    price_ac, cost_per_passenger_km, cost_breakdown, breakdown_summary, roi = market_estimations(aircraft, average_price, total_nrc, ground_time)

    # plt.figure()
    # make_loading_diagrams(aircraft)

    #####
    state = aircraft.states["cruise"]
    Cl = aircraft.mtom * g / (0.5 * state.density * state.velocity ** 2 * aircraft.WingGroup.Wing.wing_area)
    AR = aircraft.WingGroup.Wing.aspect_ratio
    alpha_horizontal_tail = np.arctan((2 * Cl)/(np.pi * AR))
    logger.debug(f"Alpha Horizontal Tail: {180 / np.pi * alpha_horizontal_tail} [deg]")
    Clh = alpha_horizontal_tail * aircraft.FuselageGroup.Tail.HorizontalTail.C_l_alpha

    AR = aircraft.FuselageGroup.Tail.HorizontalTail.aspect_ratio
    d = (aircraft.FuselageGroup.Tail.HorizontalTail.transformed_cg - aircraft.WingGroup.Wing.transformed_cg)[0]
    # print(d)
    c_avg = aircraft.FuselageGroup.Tail.HorizontalTail.mean_geometric_chord

    dCm = (1 - 4 / (AR + 2) * Clh * d) / c_avg
    print(f"dCm: {dCm} [-]")
    #####

    v_tail = aircraft.FuselageGroup.Tail.VerticalTail
    h_tail = aircraft.FuselageGroup.Tail.HorizontalTail

    logger.debug(f"###################################")
    logger.debug(f"MTOM: {aircraft.mtom:.3E} OEM: {aircraft.oem:.3E} kg, kg")
    logger.debug(f"Wing Area: {aircraft.WingGroup.Wing.wing_area:.2E} m2")
    logger.debug(f"Wing span: {aircraft.WingGroup.Wing.span:.3E} m")
    logger.debug(f"V Tail Area: {v_tail.surface_area}")
    logger.debug(f"H Tail Area: {h_tail.surface_area}")
    logger.debug(f"Fuselage Length: {aircraft.FuselageGroup.Fuselage.length} m")
    logger.debug(f"{breakdown_summary}")
    logger.debug(f"Aircraft Delivery Price [M$]: {price_ac / 1e6:.2f}")
    logger.debug(f"Competitive Aircraft Price [M$]: {competitive_price_ac / 1e6:.2f}")
    logger.debug(f"Direct Operating Cost / ASK [$/pax/km]: {cost_per_passenger_km:.4f}")
    logger.debug(f"Total Program Cost [M$]: {total_program_cost :.2f}")
    logger.debug(f"Break-even aircraft number [-]: {breakeven_point}")
    logger.debug(f"Operational ROI [%]: {roi:.2f}")
    logger.debug(f"Program ROI [%]: {program_roi:.2f}")
    logger.debug(f"Aircraft turnaround time [h]: {ground_time:.2f}")
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
    logger.debug(f"C_m_alpha: {aircraft.C_m_alpha}")
    logger.debug(f"Neutral point: {aircraft.neutral_point}")

    takeoff_speed = np.sqrt(aircraft.mtom * 9.81 / (0.5 * 1.225 * aircraft.reference_area * aircraft.C_L_TO))

    # logger.debug(f"{takeoff_speed = }")

