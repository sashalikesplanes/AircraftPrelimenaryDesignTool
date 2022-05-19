import numpy as np
# Resizing the propellors using the data from the A400M
# Imput data
csound = 343      # speed of sound [m/s]
S = 42.4          # Span [m]
V = 781/3.6       # cruise speed [m/s]
P = 32800000      # properllor power [W]
R = 4500000       # range [m]
D_fus = 5.64      # fuselage diameter [m]
P_motor = 2*10**6 # power of the electric motor [W]
T = P/V             # thrust
                    # Factor kp for typical pr0peller types
kp2 = 0.56          # 2 blades
kp3 = 0.52          # 3 blades
kp4 = 0.49          # 4 or more blades

clearance = 0.025           # distance between fuselage and engine
spacing = 0.5               # distance between enegines
n_motor = P/P_motor
group = 2
n_prop = n_motor/group
P_prop = P/n_prop
#n_prop = 18
d_prop1 = kp4 * (P_prop)**(1/4)
d_prop2 = (S-D_fus-2*clearance)/((4/3)*n_prop-(2/3))
print('numer of prop',n_prop)
print('diameter of motor',d_prop1)

