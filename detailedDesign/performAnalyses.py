import logging
import matplotlib.pyplot as plt

from detailedDesign.analysis.marketEstimations import market_estimations, production_cost_estimation, operations_and_logistics
from detailedDesign.analysis.find_stability import find_stability
from detailedDesign.sketch import sketch_aircraft
from detailedDesign.analysis.make_avl_file import make_avl_file
from detailedDesign.analysis.make_payload_range_diagram import make_payload_range_diagram
from detailedDesign.analysis.loading_diagrams import make_loading_diagrams
from detailedDesign.climbPerformance import get_max_climb_rate, get_climb_angle, get_power_plot, calc_ROC, get_theta_plot, get_heigt_velocity_plot, get_performance_altitude_plot
from detailedDesign.potatoPlot import make_potato_plot
from detailedDesign.bending_shear import find_bending_shear
import numpy as np
from misc.constants import g
from detailedDesign.analysis.dragPolar import make_drag_polar

logger = logging.getLogger("logger")


def perform_analyses(aircraft, make_stability):
    make_avl_file(aircraft)

    sketch_aircraft(aircraft)
    print_summary(aircraft)
    make_payload_range_diagram(aircraft)
    # get_power_plot(aircraft)
    # make_potato_plot(aircraft, True)
    logger.debug(f"Max climb rate obtained at a velocity of {get_max_climb_rate(aircraft)[1]} m/s\n"
                 f"Max climb rate : {get_max_climb_rate(aircraft)[0]}m/s")
    logger.debug(f'climb angle the plane can fly at take-off: {get_climb_angle(aircraft,V= aircraft.takeoff_speed)} degrees')
    logger.debug(f"ROC @ TO speed of {aircraft.takeoff_speed} m/s:{calc_ROC(aircraft, True, aircraft.takeoff_speed)}m/s")
    #get_ROC_V_plot(aircraft)

    get_performance_altitude_plot(aircraft)
    # plt.figure()
    if make_stability:
        find_stability(aircraft)

    ground_time = operations_and_logistics(aircraft)
    competitive_price_ac, total_program_cost, program_roi, average_price, total_nrc, breakeven_point = production_cost_estimation(aircraft)
    price_ac, cost_per_passenger_km, cost_breakdown, breakdown_summary, roi, revenue_per_flight, cost_per_flight = market_estimations(aircraft, average_price, total_nrc, ground_time)

    logger.debug(f"{breakdown_summary}")
    logger.debug(f"Aircraft Delivery Price [M$]: {price_ac / 1e6:.2f}")
    logger.debug(f"Competitive Aircraft Price [M$]: {competitive_price_ac / 1e6:.2f}")
    logger.debug(f"Direct Operating Cost / ASK [$/pax/km]: {cost_per_passenger_km:.4f}")
    logger.debug(f"Total Program Cost [M$]: {total_program_cost :.2f}")
    logger.debug(f"Break-even aircraft number [-]: {breakeven_point}")
    logger.debug(f"Revenue per flight [M$]: {revenue_per_flight /1e6 :.2f}")
    logger.debug(f"Cost per flight [M$]: {cost_per_flight / 1e6:.2f}")
    logger.debug(f"Operational ROI [%]: {roi:.2f}")
    logger.debug(f"Program ROI [%]: {program_roi:.2f}")
    logger.debug(f"Aircraft turnaround time [h]: {ground_time:.2f}")
    # plt.figure()
    make_loading_diagrams(aircraft)
    find_bending_shear(aircraft)

    #####
    state = aircraft.states["cruise"]
    Cl = aircraft.mtom * g / (0.5 * state.density * state.velocity ** 2 * aircraft.WingGroup.Wing.wing_area)
    AR = aircraft.WingGroup.Wing.aspect_ratio
    alpha_horizontal_tail = np.arctan((2 * Cl)/(np.pi * AR))
    logger.debug(f"Alpha Horizontal Tail: {180 / np.pi * alpha_horizontal_tail} [deg]")
    Clh = alpha_horizontal_tail * aircraft.FuselageGroup.Tail.HorizontalTail.C_l_alpha

    AR = aircraft.FuselageGroup.Tail.HorizontalTail.aspect_ratio
    d = (aircraft.FuselageGroup.Tail.HorizontalTail.transformed_cg - aircraft.WingGroup.Wing.transformed_cg)[0]

    c_avg = aircraft.FuselageGroup.Tail.HorizontalTail.mean_geometric_chord

    dCm = (1 - 4 / (AR + 2) * Clh * d) / c_avg
    print(f"dCm: {dCm} [-]")
    #####

    make_drag_polar(aircraft)

    plt.show()


def print_summary(aircraft):

    v_tail = aircraft.FuselageGroup.Tail.VerticalTail
    h_tail = aircraft.FuselageGroup.Tail.HorizontalTail

    logger.debug(f"###################################")
    logger.debug(
        f"MTOM = {aircraft.mtom:.4E} kg, OEM = {aircraft.oem:.4E} kg, Fuel Mass = {aircraft.fuel_mass:.4E}")
    logger.debug(f"Wing Area: {aircraft.WingGroup.Wing.wing_area:.2E} m2")
    logger.debug(f"Wing span: {aircraft.WingGroup.Wing.span:.3E} m")
    logger.debug(f"V Tail Area: {v_tail.surface_area}")
    logger.debug(f"H Tail Area: {h_tail.surface_area}")
    logger.debug(f"Fuselage Length: {aircraft.FuselageGroup.Fuselage.length} m")
    logger.debug(f"{aircraft.cruise_drag = :.4E} N")
    logger.debug(f"Wing Area: {aircraft.reference_area:.2f} m2")
    logger.debug(f"INOP Moment: {aircraft.WingGroup.Engines.engines_inoperative_moment} Nm")

    fuselage = aircraft.FuselageGroup.Fuselage
    logger.debug(f"Cockpit length: {fuselage.cockpit_length} m")
    logger.debug(f"Cabin length: {fuselage.Cabin.length} m")
    logger.debug(f"Ass length: {fuselage.AssFuelContainer.length} m")
    logger.debug(f"Tail cone length: {fuselage.tail_length} m")
    logger.debug(f"Fuselage Length: {fuselage.length} m")
    logger.debug(f"Forward fuel length: {fuselage.ForwardFuelContainer.length} m")
    logger.debug(f"Aft fuel length: {fuselage.AftFuelContainer.length} m")
    logger.debug(f"TOtal volume :{fuselage.ForwardFuelContainer.volume_tank + fuselage.AftFuelContainer.volume_tank + fuselage.AssFuelContainer.volume_tank}")

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

    logger.debug(f"Volume of fuel cells {aircraft.FuselageGroup.Power.FuelCells.size} m^3")

    engines = aircraft.WingGroup.Engines
    logger.debug(f"Reference Thrust Cruise {aircraft.reference_cruise_thrust}")
    logger.debug(f"Reference Thrust Takeoff {aircraft.reference_takeoff_thrust}")
    logger.debug(f"C_m_alpha: {aircraft.C_m_alpha}")
    logger.debug(f"Neutral point: {aircraft.neutral_point}")
    logger.debug(f"C_g position: {aircraft.cg_loaded_half_fuel}")
    logger.debug(f"x_ac : {aircraft.WingGroup.Wing.x_aerodynamic_center}")

    logger.debug(f"##########################################################")
    logger.debug(f"##### FOR PALOMA AND JULIE!!!! ###########################")
    logger.debug(f"##########################################################")
    logger.debug(f"ENGINES:")
    logger.debug(f"Diameter fans: {engines.own_diameter_fan}")
    logger.debug(f"N fans on wing: {engines.own_fans_on_wing}")
    logger.debug(f"N fans on fus: {engines.own_fans_on_fuselage}")
    logger.debug(f"Length unit {engines.own_lenght_unit} m, i think")
    logger.debug(f"Length fan {engines.own_length_fan} m, i think")
    logger.debug(f"Spacing: {engines.own_spacing} m")


    logger.debug(f"WING:")
    logger.debug(f"Wing span: {aircraft.WingGroup.Wing.span} m")
    logger.debug(f"Ailerons length: {aircraft.WingGroup.Wing.length_ailerons} m")
    logger.debug(f"Root chord: {aircraft.WingGroup.Wing.root_chord} m")
    logger.debug(f"Tip chord: {aircraft.WingGroup.Wing.tip_chord} m")
    logger.debug(f"LE Sweep: {aircraft.WingGroup.Wing.leading_edge_sweep} rad")
    h_tail = aircraft.FuselageGroup.Tail.HorizontalTail
    logger.debug(f"H TAIL:")
    logger.debug(f"Root chord: {h_tail.root_chord} m")
    logger.debug(f"Tip chord: {h_tail.tip_chord} m")
    logger.debug(f"Span: {h_tail.span} m")
    logger.debug(f"LE Sweep: {h_tail.leading_edge_sweep} rad")
    v_tail = aircraft.FuselageGroup.Tail.VerticalTail
    logger.debug(f"V TAIL:")
    logger.debug(f"Root chord: {v_tail.root_chord} m")
    logger.debug(f"Tip chord: {v_tail.tip_chord} m")
    logger.debug(f"Span: {v_tail.span} m")
    logger.debug(f"LE Sweep: {v_tail.leading_edge_sweep} rad")



    takeoff_speed = np.sqrt(aircraft.mtom * 9.81 / (0.5 * 1.225 * aircraft.reference_area * aircraft.C_L_TO))

    # logger.debug(f"{takeoff_speed = }")

