import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import pandas as pd
from pathlib import Path

from misc.constants import g
from detailedDesign.board_passengers import board_passengers
from detailedDesign.classes.Loads import *
from detailedDesign.bending_shear import open_df


dx = 0.1


def make_loading_diagrams(aircraft):
    make_wing_loading_diagrams(aircraft)
    make_aircraft_loading_diagrams(aircraft)


def make_wing_loading_diagrams(aircraft):
    # Try to open the dataframe in order to generate it if it is not present
    open_df()

    df_location = Path('data', 'dataframes', 'wing_loading.dat')
    lift = LiftCurve(df_location, aircraft.mtom * g / 2)
    lift.calc_shear(100)

    # Make the liftcurve and the linear load
    span = aircraft.WingGroup.Wing.span / 2
    total_length = span
    m_wing = aircraft.WingGroup.Wing.own_mass
    lift_fus = (aircraft.mtom - m_wing) * g
    df_location = Path('data', 'dataframes', 'wing_loading.dat')
    forces = [PointLoad(0, -lift_fus), LiftCurve(df_location, lift_fus + m_wing * g), LinearLoad([span / 2, 0, 0], -m_wing * g, span)]

    # Initialize a new figure
    fig, (ax1, ax2) = plt.subplots(2)

    # Calculate shear and bending over the longitudinal plane length
    X = np.arange(0, total_length, dx)
    shear = np.array([sum([i.calc_shear(y) for i in forces]) for y in X])
    # moment = -np.array([sum([i.calc_moment(y) for i in forces]) for y in X])

    # Plot the bending and shear diagram
    ax1.set_title("Wing Shear Loading Diagram")
    ax1.set(xlabel="Longitudinal Position [m]", ylabel="Shear Force [kN]")
    ax1.plot(X, shear * -10 ** -3, color="tab:red")
    ax1.grid()

    moment_integral = integrate.cumtrapz(shear, X, initial=0, dx=dx)
    moment_integral = moment_integral - moment_integral[-1]

    ax2.set_title("Wing Bending Diagram")
    ax2.set(xlabel="Longitudinal Position [m]", ylabel="Bending Moment [kNm]")
    # ax2.plot(X, moment * 10 ** -3, color="tab:green")
    ax2.plot(X, np.array(moment_integral) * -10 ** -3, "-", color="tab:green")
    ax2.grid()

    aircraft.WingGroup.Wing.span_wise_shear = shear
    aircraft.WingGroup.Wing.span_wise_moment = moment_integral


def make_aircraft_loading_diagrams(aircraft):
    """Make the loading diagram"""
    # Board the payload and fuel into the aircraft
    aircraft = board_passengers(aircraft)

    # Make the different components to find forces from
    fuselage_group = aircraft.FuselageGroup
    components = get_sizes_and_loads(fuselage_group)
    forces = []

    # Initialize the bending moment due to the wing
    # print(aircraft.WingGroup.Wing.get_C_m(aircraft.WingGroup.Wing.installation_angle))
    # print(0.075)
    # this number is made negative since the coordinate system for the moment diagram is inverted
    C_m = -aircraft.WingGroup.Wing.get_C_m(aircraft.WingGroup.Wing.installation_angle)
    state = aircraft.states["cruise"]
    wing_area = aircraft.WingGroup.Wing.wing_area
    normalized_chord = aircraft.WingGroup.Wing.mean_geometric_chord
    moment = 0.5 * state.density * state.velocity ** 2 * wing_area * C_m * normalized_chord
    forces.append(PointMoment(aircraft.WingGroup.Wing.transformed_cg, moment))

    # TODO: introduce tail forces in order to finalize moment diagram
    C_mh = -0.4079129718445125
    S_h = aircraft.FuselageGroup.Tail.HorizontalTail.surface_area
    C_h = aircraft.FuselageGroup.Tail.HorizontalTail.mean_geometric_chord
    moment = 0.5 * state.density * state.velocity ** 2 * S_h * C_mh * C_h
    # forces.append(PointMoment(aircraft.FuselageGroup.Tail.HorizontalTail.transformed_cg, -moment))

    # Transform the components into the correct loads
    for component in components:
        if component[2] is None:
            forces.append(PointLoad(component[3], -component[1] * g))
        else:
            forces.append(DistributedLoad(component[3], -component[1] * g, component[2]))

    # Get the maximum length to plot to
    total_length = aircraft.FuselageGroup.Tail.transformed_pos[0]

    # Lift force
    lift = PointLoad(aircraft.WingGroup.Wing.transformed_cg[0], aircraft.FuselageGroup.get_mass() * g)
    forces.append(lift)

    # Plot the forces for debugging
    # plt.figure()
    # [x.plot() for x in forces]
    # plt.title("Forces Drawing")

    # Initialize a new figure
    fig, (ax1, ax2) = plt.subplots(2)

    # Calculate shear and bending over the longitudinal plane length
    X = np.arange(0, total_length, dx)
    shear = np.array([sum([i.calc_shear(y) for i in forces]) for y in X])
    moment = -np.array([sum([i.calc_moment(y) for i in forces]) for y in X])

    absolute_shear = abs(shear * 10 ** -3)
    max_abs_shear = max(absolute_shear)
    shear_cut1 = max_abs_shear/3
    shear_cut2 = max_abs_shear*2/3

    # Plot the bending and shear diagram
    ax1.set_title("Fuselage Shear Loading Diagram")
    ax1.set(xlabel="Longitudinal Position [m]", ylabel="Shear Force [kN]")
    ax1.plot(X, shear * 10 ** -3, color="tab:red", label="Shear Force")
    ax1.plot(X, absolute_shear, "--", color="tab:red", label="Absolute Shear Force")
    ax1.hlines([shear_cut1], 0, aircraft.FuselageGroup.Fuselage.length, colors="tab:red",
               linestyles='dashdot')
    ax1.hlines([shear_cut2], 0, aircraft.FuselageGroup.Fuselage.length, colors="tab:red", linestyles='dashdot')
    ax1.grid()

    # moment_integral = integrate.cumtrapz(shear, X, initial=0, dx=dx)

    ax2.set_title("Fuselage Bending Diagram")
    ax2.set(xlabel="Longitudinal Position [m]", ylabel="Bending Moment [kNm]")
    ax2.plot(X, moment * 10 ** -3, color="tab:green")
    # ax2.plot(X, np.array(moment_integral) * 10 ** -3, "--", color="tab:green")
    ax2.grid()

    aircraft.FuselageGroup.Fuselage.longitudinal_shear = shear
    aircraft.FuselageGroup.Fuselage.longitudinal_moment = moment


def get_sizes_and_loads(head_component):
    if hasattr(head_component, "length"):
        l = head_component.length
    else:
        l = None

    if str(head_component) == "Miscellaneous":
        lst = head_component.forces_lst
        total_accounted_mass = sum([x[1] for x in lst])
        lst.append(("RemainingMisc", head_component.cow_mass - total_accounted_mass, l, head_component.FuselageGroup.Fuselage.transformed_cg))
        return lst

    lst = [(str(head_component), head_component.cow_mass, l, head_component.transformed_cg)]
    for component in head_component.components:
        lst += get_sizes_and_loads(component)
    return lst
