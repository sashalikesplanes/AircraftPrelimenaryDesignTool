# Stability
import numpy as np
import matplotlib.pyplot as plt


AR = 10.619#8
ARh = 4.57# 5
M = 0.82 #0.61
eta = 0.95
halfchordsweep = 0.384 #0.001  # rad approx
halfchordsweeph = 10/180*np.pi # approx [rad]


bf = 2.69 #12  #width of fuselage
hf = 2.69 #12
lfn = 36.57# 100 # approx length of fuselage
b = 26.17# 120
croot = 3.48 #21
S = 77.39#2326
taperratio = 0.2485 #0.852
quarterchordsweep = 0.4564# 0  # [rad]
Snet = S-croot*(1+taperratio+(b-bf)/b)*bf/2  # Surface area wing - area inside the fuselage
lh = 17.3#50  # approx
cMAC = 3.48# 19.73
cMGC = 3.19 #19.73
VhoverV = 1#0.85  # if fuselage mounted
SM = 0.05
Xacw = 0.22
kn = -4.0


def calc_CLalpha(aspect_ratio, beta, semi_chord_sweep):
    C_L_alpha = 2 * np.pi * aspect_ratio / (2 + np.sqrt(((aspect_ratio*beta) / eta) ** 2\
                * (1 + np.tan(semi_chord_sweep) ** 2 / (beta ** 2)) + 4))
    return C_L_alpha

beta = np.sqrt(1-M**2)
dedalpha =4/(AR+2)
CLalphawing = calc_CLalpha(AR, beta, halfchordsweep)
CLalphatail = calc_CLalpha(ARh, beta, halfchordsweeph)
CLalphatailless = CLalphawing*(1+2.15*bf/b)*Snet/S+np.pi/2*bf**2/S
Xacwf = Xacw -1.8/CLalphatailless*bf*hf*lfn/S/cMAC+0.273/(1+taperratio)*bf*cMGC*(b-bf)/cMAC**2*(b+2.15*bf)*np.tan(quarterchordsweep)
'''In the code the contribution of the nacelles to Xacwf is neglected as it is -0.0003 per engine'''

print('deda=', dedalpha, 'CLaw=', CLalphawing, 'CLah=', CLalphatail)
print("Xac/c=",Xacwf)
print(1.8/CLalphatailless*bf*hf*lfn/S/cMAC)
Xcg = np.arange(0,1,0.05)
print(Xcg)

STABILITYTERM = CLalphatail/CLalphatailless*(1-dedalpha)*lh/cMAC*VhoverV**2
ShoverS = 1/STABILITYTERM*Xcg-(Xacwf-SM)/STABILITYTERM

plt.plot(Xcg,ShoverS)
plt.xlabel("xcg/c")
plt.ylabel("Sh/S")
plt.grid()
plt.show()