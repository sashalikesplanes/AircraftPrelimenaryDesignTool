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

    # df_location = Path('data', 'dataframes', 'wing_loading.dat')
    # lift = LiftCurve(df_location, aircraft.mtom * g / 2)
    # lift.calc_shear(100)

    # Make the liftcurve and the linear load
    span = aircraft.WingGroup.Wing.span / 2
    total_length = span
    m_wing = aircraft.WingGroup.Wing.own_mass
    m_engines = aircraft.WingGroup.Engines.own_mass
    lift_fus = (aircraft.mtom - m_wing - m_engines) * g / 2
    df_location = Path('data', 'dataframes', 'wing_loading.dat')
    forces = [PointLoad(0, -lift_fus), LiftCurve(df_location, lift_fus + (m_wing + m_engines) * g / 2), LinearLoad([span / 2, 0, 0], -m_wing * g / 2, span)]

    # Find the amount of engines in order to model the engines as point loads
    n_engines = int(np.ceil(aircraft.WingGroup.Engines.own_amount_fans))
    spacing_engine = aircraft.WingGroup.Engines.own_spacing

    m_engine = m_engines / n_engines

    y_leftmost_engine = -(n_engines - 1) * spacing_engine / 2
    for i in range(n_engines):
        y_current = y_leftmost_engine + i * spacing_engine
        if y_current > 0:
            forces.append(PointLoad(y_current, m_engine * g))
        elif y_current == 0:
            forces.append(PointLoad(y_current, m_engine * g / 2))

    # Initialize a new figure
    fig, (ax1, ax2) = plt.subplots(2)

    # Calculate shear and bending over the longitudinal plane length
    X = np.arange(0, total_length, dx)
    shear = np.array([sum([i.calc_shear(y) for i in forces]) for y in X])

    # TODO: fix the shear in a less hacky way
    shear = shear - shear[-1]
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
               linestyles="dashdot", label="Design Section Cutoffs")
    ax1.hlines([shear_cut2], 0, aircraft.FuselageGroup.Fuselage.length, colors="tab:red", linestyles='dashdot')
    ax1.legend()
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

def wingbox(aircraft):
    step = 0.1
    span = aircraft.WingGroup.Wing.span
    b = np.arange(0, span/2, step)
    linestyles = ['-','--','-.',':']
    tvariation = np.arange(0.002, 0.006,0.001)
    for t in tvariation:
        listtosavestringers = []
        listtosavestringersmom = []
        for y in b:
            croot = aircraft.WingGroup.Wing.root_chord
            taper = aircraft.WingGroup.Wing.taper_ratio
            chord = croot * (1 + 2 * (taper - 1) / span * y)
            l = 0.5 * chord
            h = 0.0876 * chord  # from Catia
            index = np.where(b == y)
            V = aircraft.WingGroup.Wing.span_wise_shear[index]#-10000000  # from max dependent on span loc
            Astringer = 0.012  # based on sample report but should be elaborated
            # Ixxbox = l*h**3/12-(l-2*t)*(h-2*t)**3/12 # Ixx of the box
            # Ixxstringer = Astringer*(h/2-t)**2
            # n_stringer = 8 #TODO get a reasonable value
            # Ixx = Ixxbox+n_stringer*Ixxstringer
            tauallow = 331 * 10 ** 6/1.5/1.2  # Al7075 +1.5 safety +1.2 for torque
            slist = np.arange(0, l + h, step)
            Ixxlist = []
            for s in slist:
                if s <= 0.5 * l:
                    Ixx = -V / tauallow * (0.5 * h * s)
                if 0.5 * l < s <= 0.5 * l + h:
                    sfix = 0.5 * l
                    s = s - sfix
                    Ixx = -V / tauallow * (0.5 * h * sfix) + -V / tauallow * (0.5 * h * s - 0.5 * s ** 2)
                if 0.5 * l + h < s <= l + h - step:
                    sfix1 = 0.5 * l
                    sfix2 = h
                    s = s - (sfix1 + sfix2)
                    Ixx = -V / tauallow * (0.5 * h * sfix1) + -V / tauallow * (
                                0.5 * h * sfix2 - 0.5 * sfix2 ** 2) + - V / tauallow * (-0.5 * h * s)
                Ixxlist.append(Ixx)
            Ixxmax = np.max(Ixxlist)
            n_stringerlist = np.arange(0, 15, 1)
            #t= 0.004 #4 mm
            #print(f"b:{y},index:{index}v:{V},Ixxneeded:{Ixxmax-t * (6 * l * h ** 2 + 2 * h ** 3) / 12}, I per stringer:{Astringer * (h / 2) ** 2} ")

            # for n_stringer in n_stringerlist:
            #     I = t * (6 * l * h ** 2 + 2 * h ** 3) / 12
            #     Ixxneeded = Ixxmax - I
            #     if Ixxneeded < Astringer * (h / 2) ** 2 * n_stringer:
            #         listtosavestringers.append(n_stringer)

            Ibox = t * (6 * l * h ** 2 + 2 * h ** 3) / 12
            Ixxneeded = Ixxmax - Ibox
            n_stringer = 0
            while Ixxneeded > Astringer * (h / 2) ** 2 * n_stringer:
                n_stringer += 1
            #print(f"for a span of {y}, the stringers needed are: {n_stringer}")
            listtosavestringers.append(n_stringer)
            # print(f"for a span of {y}, the stringers needed are: {listtosavestringers[0]}")
            moment = aircraft.WingGroup.Wing.span_wise_moment[index] # this is somehow positive
            distancetop = h / 2
            maximumstressbottom = 503 * 10 ** 6 / 1.5  # TODO check
            Ixxwanted = moment * distancetop / maximumstressbottom
            # print(f"h:{h}, l:{l}")
            # print(f"Ixxbox:{Ibox},Istringer: {Astringer * (h / 2) ** 2}")
            # print(f"Ixxwanted:{Ixxwanted} M:{moment}")
            n_sttringer = 0
            while Ixxwanted-Ibox > Astringer * (h / 2) ** 2 * n_sttringer:
                n_sttringer += 1
            #print(f"for a span of {y}, the stringers needed are: {n_sttringer}")
            listtosavestringersmom.append(n_sttringer)
        linestyleindex = int(np.where(tvariation == t)[0])
        plt.plot(b,listtosavestringers, label = f"t = {t*1000} [mm]", ls = linestyles[linestyleindex])
        #plt.plot(b,listtosavestringersmom, label = f"t = {t*1000} [mm]", ls = linestyles[linestyleindex])
    for i in range(len(listtosavestringersmom)):
        listtosavestringersmom[i] = 2 * np.ceil((listtosavestringersmom[0] + 1) / 2)
        # if i < 0.25 * len(listtosavestringersmom):
        #     listtosavestringersmom[i] = 2*np.ceil((listtosavestringersmom[0]+1)/2)
        # if 0.25 * len(listtosavestringersmom) <= i < 0.5 * len(listtosavestringersmom):
        #     listtosavestringersmom[i] = 2*np.ceil((listtosavestringersmom[int(0.25*len(listtosavestringersmom))]+1)/2)
        # else:
        #     listtosavestringersmom[i] = 2 * np.ceil((listtosavestringersmom[i] + 1) / 2)
    plt.plot([0,15.72,15.72,31.44,31.44,47.16,47.16,62.89],[10,10,6,6,2,2,2,2],label = 'Chosen amount of stringers', lw = 3)
    #plt.plot([0,15.72,15.72,31.44,31.44,47.16,47.16,62.89],[50,50,28,28,8,8,2,2],label = 'Chosen amount of stringers', lw = 3)
    #plt.plot(b,listtosavestringersmom, label = 'Chosen amount of stringers', lw = 3)
    plt.title("Stringers needed at different spanwise locations")
    plt.xlabel("Half span [m]")
    plt.ylabel("Number of stringers needed [-]")
    plt.grid()
    plt.legend()
    plt.show()
            #tlist.append(t)


        # plt.scatter(n_stringerlist,tlist)
        # plt.title("hello")
        # plt.show()

        # for n_stringer in n_stringerlist:
        #
        #     tlist = np.arange(0, 15, 0.001)
        #     Ixxlistq = []
        #     for t in tlist:
        #         Ixxthick = (6 * l * h ** 2 + 2 * h ** 3) / 12 * t / 1000
        #         Ixxstr = Astringer * (h / 2) ** 2 * n_stringer
        #         Ixxlistq.append((Ixxthick + Ixxstr))
        #     plt.plot(tlist, Ixxlistq, label=f"number of stringers = {n_stringer}")
        #
        #     plt.title("k")
        # plt.plot([0, 15], [Ixxmax, Ixxmax])
        # plt.legend()
        # plt.show()

        #plt.plot(slist, Ixxlist)
        # plt.plot([0.5*l,0.5*l],[0,-230], 'r')
        # plt.plot([0.5*l+h,0.5*l+h],[0,-230], 'r')

        #plt.show()

