import numpy as np

pr = 1.9           # pressure ratio
flow_coef = 0.5     # whittle fan
omega = 2500 * 2* np.pi / 60  # rpm of the emotor from 2500 to 1800

rho =  0.8194       # kg/m3 for 4000 m
#rho = 0.259814     #A380

Ps = 61640.24       # Pa static pressure at 4000 m
#Ps = 16157.9       #A380

Tt = 659256.83
#Tt = 53500 * 4.44822 * 4  # from propeller sizing example
#Tt = 4 * 70000 * 4.44822 # N A380

V0 = 500 / 3.6      # m/s cruise speed
#V0 = 900/3.6    # m/s A380

P_motor = 4000000   # W
eff_mot_inv = 0.95  #

P_aircraft = Tt * V0
n_fans = P_aircraft/(P_motor * eff_mot_inv)

Tf = Tt/n_fans
Pt0 = Ps + 0.5 * rho * V0**2
Pt1 = Pt0 * pr
V1 = np.sqrt(2*(Pt1 - Ps) / rho)
m_dot = Tf / (V1-V0)

# Ut = omega * r
# A = m_dot / (flow_coef * rho * Ut)
# A = np.pi * r
r = (m_dot/ (flow_coef * rho * np.pi * omega)) ** (1/3)


# get the weight of ducted fan
d = 2*r
weight = 0.0004*d**2 + 0.0554*d - 2.064



print ('radius of a fan', r)
print ('number of fans', n_fans)
print ('Minimum wing span (not accounting for fuselage) ', n_fans*2*r)
print ('blade tip speed', omega*r)