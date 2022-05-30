# Stability
import numpy as np
import matplotlib.pyplot as plt


AR = 8
ARh = 5
M = 0.61
eta = 0.95
halfchordsweep = 0.001  # rad approx
halfchordsweeph = 10 / 180 * np.pi  # approx [rad]

bf = 12  #width of fuselage
hf = 12
lfn = 100 # approx length of fuselage
b = 120

S = 2326
taperratio = 0.852
quarterchordsweep = 0  # [rad]
lh = 50  # approx
croot = 2*S/((1+taperratio)*b)
ctip = taperratio*croot
Snet = S - croot * (1 + taperratio + (b - bf) / b) * bf / 2  # Surface area wing - area inside the fuselage
cMAC = 19.73
cMGC = 19.73
VhoverV = 0.85  # if fuselage mounted
SM = 0.05
Xacw = 0.22
kn = -4.0
print(croot,ctip)

def calc_CLalpha(aspect_ratio, beta, semi_chord_sweep):
    C_L_alpha = 2 * np.pi * aspect_ratio / (2 + np.sqrt(4 + ((aspect_ratio * beta) / eta) ** 2 \
                                                        * (1 + np.tan(semi_chord_sweep) ** 2 / (beta ** 2))))
    return C_L_alpha


beta = np.sqrt(1 - M ** 2)
dedalpha = 4 / (AR + 2)
CLalphawing = calc_CLalpha(AR, beta, halfchordsweep)
CLalphatail = calc_CLalpha(ARh, beta, halfchordsweeph)
CLalphatailless = CLalphawing * (1 + 2.15 * bf / b) * Snet / S + np.pi / 2 * bf ** 2 / S
Xacwf = Xacw - 1.8 / CLalphatailless * bf * hf * lfn / S / cMAC + 0.273 / (1 + taperratio) * bf * cMGC * (b - bf) / (
            cMAC ** 2 * (b + 2.15 * bf)) * np.tan(quarterchordsweep)
'''In the code the contribution of the nacelles to Xacwf is neglected as it is -0.0003 per engine'''

print('deda=', dedalpha, 'CLaw=', CLalphawing, 'CLah=', CLalphatail)
print("CLalpha A-h =", CLalphatailless)
print("Xac/c=", Xacwf)
print(1.8 / CLalphatailless * bf * hf * lfn / S / cMAC)
Xcg = np.arange(-1, 1, 0.05)
print(Xcg)
print('snet',Snet)

STABILITYTERM = CLalphatail / CLalphatailless * (1 - dedalpha) * lh / cMAC * VhoverV ** 2
ShoverSstability = 1 / STABILITYTERM * Xcg - (Xacwf - SM) / STABILITYTERM

plt.plot(Xcg, ShoverSstability)
plt.xlabel("xcg/c")
plt.ylabel("Sh/S")
plt.grid()
#plt.show()

'''From here controllability, controllability is sized for landing'''

CLh = -0.8  # from slide 17 lecture 8
Wfin  = 1879000*9.81
Vlanding = 77  # from boeing 787
rho_sealevel = 1.225
CLaminush = Wfin/(0.5*rho_sealevel*Vlanding**2*S)

###'''Cmaerodynamiccentre calculation'''###
#wing
Cm0foil = 1
Cmaerocwing = Cm0foil*(AR*np.cos(quarterchordsweep)**2/(AR+2*np.cos(quarterchordsweep)))  # sweep assumed quarter chord sweep

#fuselage
CL0 = 1  # CL0 is the lift coefficient of the flapped wing at zero angle of attack
betaslow = 1
CLalphataillessslow = calc_CLalpha(AR,betaslow,halfchordsweep)
deltafus_Cmaeroc = -1.8*(1-2.5*bf/lfn)*np.pi*bf*hf*lfn/(4*S*cMAC)*CL0/CLalphataillessslow

#flaps
deltaClmax = 1.45+0.56  # added 0.56 for droop nose. Check for correctness
xf = 0.019*cMAC # 0.019 from Snorri book page 422 NACA651213
cprimeoverc = (cMAC+xf)/cMAC
deltaCLmax = 1.1*0.975*1*1.3  # from DATCOM 1978 eq8.4
sweephingeline = 0
Swf = deltaCLmax*S/(0.9*deltaClmax*np.cos(sweephingeline))

cfoverc = 0.336
cfovercprime = cfoverc/cprimeoverc
print('cfcprime', cfovercprime)
flappedspan = 46.135*2
flappedspanoverb = flappedspan/b

mu1 = 0.17  # mu comes from graphs
mu2 = 0.8

CLwing = Wfin/(0.5*rho_sealevel*Vlanding**2*S)
#print('Swf=',Swf, 'flapoverb', flappedspanoverb)


deltaCmquarter = mu2*(-mu1*deltaClmax*cprimeoverc-(CLwing+deltaClmax*(1-Swf/S))/8*cprimeoverc*(cprimeoverc-1))  #neglecting sweep term
deltaf_Cmaeroc = deltaCmquarter-CLwing*(0.25-Xacwf)
Cmaeroc = Cmaerocwing + deltaf_Cmaeroc + deltafus_Cmaeroc  # + deltanac_Cmaeroc, neglecting nacelles for now
print('Cmac', Cmaeroc)

CONTROLLABILITYTERM = CLh / CLaminush * lh / cMAC * VhoverV ** 2

ShoverScontrollability = 1 / CONTROLLABILITYTERM * Xcg + (Cmaeroc / CLaminush - Xacwf) / CONTROLLABILITYTERM

plt.plot(Xcg,ShoverScontrollability)
plt.ylim(0,1)
plt.show()
