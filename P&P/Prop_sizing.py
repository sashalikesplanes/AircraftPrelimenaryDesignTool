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
    m_specific_motor = 10000          # [W/kg] for the 2MW motor
    d_motor = 0.46              # [m] diameter of the 2MW motorusing the coca-cola method
    l_motor = 1.1               # [m] length of a motor
    clearance = 0.025           # distance between fuselage and engine from literature
    m_propellor = 535.9418132   # [kg] from the excel extrapollation

    # Calculations
    P_aircraft = T*V                             # power the aircraft needs  [W]
    n_motor = np.ceil((P_aircraft/P_motor)/2)*2  # we want an even number of propelors
    n_prop = np.ceil((P_aircraft/P_eng)/2)*2
    group = np.ceil(n_motor/n_prop)              # amount of motors per propellor
    l_min_group_motor = group * l_motor   # [m] asuming they are connected in series
    S_fit = n_prop * D_prop_an22 +2*clearance + (1/3)* D_prop_an22 * (n_prop-2) + D_fus   # ideal span to fit all propellers needed
    if S_fit > S :
        print('The propellors dont fit in the Span. The span should be at least', S_fit, 'but it is', S)
    d_prop = (S-D_fus-2*clearance)/((4/3)*n_prop-(2/3))  # from the geometry with spacing of 1/3 of d_prop
    m_motors = P_aircraft / m_specific_motor  #mass of the motors needed to produce the thrust
    vol_motor = d_motor * d_motor * l_motor    # [m3] the volume is calculated as if the motor had a box like shape instead of being a cilinder
    m_prop_motors = m_motors + m_propellor

    print('number of motors per propellor', group)
    print('numer of prop', n_prop)
    print('max diam of prop according to geometry in m', d_prop)
    print('number of motor', n_motor)
    print('mass of motors in kg', m_motors)
    print('mass of motors plus prop', m_prop_motors)
    print('min length of group of motor ', l_min_group_motor)
    print('vol of one motor', vol_motor)

    return n_prop, m_prop_motors , l_min_group_motor, vol_motor

import numpy as np
S = 100                     # Span [m]
V = 500 / 3.6               # cruise speed [m/s]
T = 53500 * 4.44822 * 4     # [N]thrust the times 4 is for having 4 engines in our example
D_fus = 6                   # fuselage diameter [m]
a = propellor_sizing(S,V,T,D_fus)
print(a)