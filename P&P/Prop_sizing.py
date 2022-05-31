def propellor_sizing(Span, V_cuise, Thrust, Diameter_fuselage):
    # Redefine variables
    S = Span
    V = V_cuise
    T = Thrust
    D_fus = Diameter_fuselage

    # Ref aircraft An-22 data
    P_eng = 11000000             #[W] Power of one engine of the An-22
    D_prop_an22 = 5.6            #[m] diameter of propellor of An-22

    # Constants
    P_motor = 2*10**6           # power of the electric motor [W]
    m_specific_motor = 10000    # [W/kg] for the 2MW motor
    d_motor = 0.46              # [m] diameter of the 2MW motorusing the coca-cola method
    l_motor = 0.8               # [m] length of a motor
    clearance = 0.025           # distance between fuselage and engine from literature
    m_propellor = 535.9418132   # [kg] from the excel extrapollation
    l_inverter= 0.46
    m_specific_inverter= 30000  # [W/kg]
    vol_specific_inverter= 20000000  # [W/m3]
    eff_inverter= 0.995

    # conting and eff
    eff_gearbox= 0.9  # efficiency of a gearbox connection
    spacing_motor_contingency= 1.15
    height_unit_contingency= 1.5
    gearbox_unit_vol_contingency= 1.1
    gearbox_unit_mass_contingency= 1.2
    width_gearbox_contingency= 1.3


    # Calculations
    P_aircraft = T * V  # power the aircraft needs  [W]
    group = np.ceil(P_eng / (P_motor * eff_gearbox))  # amount of motors per propellor
    n_prop = np.ceil(P_aircraft / P_eng)
    n_motor = group * n_prop
    # n_prop = np.ceil((P_aircraft/P_eng)/2)*2    # we want an even number of propelors
    # n_motor = np.ceil((group * n_prop)/2)*2

    length_unit = np.ceil(group / 2) * d_motor * spacing_motor_contingency  # [m] asuming they are connected in series
    width_unit = 2 * (l_motor + l_inverter) * width_gearbox_contingency
    height_unit = d_motor * height_unit_contingency

    S_fit = n_prop * D_prop_an22 + 2 * clearance + (1 / 3) * D_prop_an22 * (
            n_prop - 2) + D_fus  # ideal span to fit all propellers needed
    n_prop_fit = np.floor((S - 2 * clearance - D_fus + (2 / 3) * D_prop_an22) / (
            (4 / 3) * D_prop_an22))  # amount of propellors needed to fit in the desired span

    if S_fit > S:
        print('The propellors dont fit in the Span. The span should be at least', S_fit, 'but it is', S,
              '. The maximun amount of propellors that fit in the span of S=', S, 'is n_max_prop=', n_prop_fit)

    d_max_prop = (S - D_fus - 2 * clearance) / (
                (4 / 3) * n_prop - (2 / 3))  # from the geometry with spacing of 1/3 of d_prop

    m_motor = P_motor / m_specific_motor  # mass of the motors needed to produce the thrust
    vol_motor = d_motor * d_motor * l_motor  # [m3] the volume is calculated as if the motor had a box like shape instead of being a cilinder

    m_inverter = P_motor / m_specific_inverter
    vol_inverter = P_motor / vol_specific_inverter

    vol_unit = group * (vol_motor + vol_inverter) * gearbox_unit_vol_contingency
    vol_total = n_prop * vol_unit
    m_unit = ((m_motor + m_inverter) * group + m_propellor) * gearbox_unit_mass_contingency
    m_total = n_prop * m_unit


    #print('number of motors per propellor', group)
    print('numer of prop needed', n_prop)
    #print('max diam of prop according to geometry in m', d_max_prop)
    #print('number of motor', n_motor)
    #print('mass of motors in kg', m_allmotors)
    #print('mass of motors plus prop', m_pm)
    #print('min length of group of motor ', l_min_group_motor)
    #print('vol of one motor', vol_motor)

    print('total mass', m_total)
    print('lenght unit',length_unit)
    print('width unit', width_unit)
    print('height unit', height_unit)
    print('total mass', m_total)
    print('power',P_aircraft)
    return


import numpy as np
S = 100                    # Span [m]
V = 500 / 3.6               # cruise speed [m/s]
T = 53500 * 4.44822 * 4     # [N]thrust the times 4 is for having 4 engines in our example
D_fus = 6                   # fuselage diameter [m]
a = propellor_sizing(S,V,T,D_fus)
