# Stability
import numpy as np
import matplotlib.pyplot as plt




def calc_Snet(S, croot, taperratio, b, widthfuselage):
    Snet = S - croot * (1 + taperratio + (
            b - widthfuselage) / b) * widthfuselage / 2  # Surface area wing - area inside the fuselage
    return Snet


def calc_CLalpha(aspect_ratio, beta, semi_chord_sweep):
    C_L_alpha = 2 * np.pi * aspect_ratio / (2 + np.sqrt(4 + ((aspect_ratio * beta) / eta) ** 2
                                                        * (1 + np.tan(semi_chord_sweep) ** 2 / (beta ** 2))))
    return C_L_alpha


def calc_beta(M):
    beta = np.sqrt(1 - M ** 2)
    return beta


def calc_depsilondalpha(AR):
    depsilondalpha = 4 / (AR + 2)
    return depsilondalpha


def calc_Xacwf(Xacw, CLalphatailless, widthfuselage, heightfuselage, lengthfuselage, S, cMAC, taperratio, cMGC, b,
               quarterchordsweep):
    Xacwf = Xacw - 1.8 / CLalphatailless * widthfuselage * heightfuselage * lengthfuselage / S / cMAC + 0.273 / (
            1 + taperratio) * widthfuselage * cMGC * (b - widthfuselage) / (
                    cMAC ** 2 * (b + 2.15 * widthfuselage)) * np.tan(quarterchordsweep)
    return Xacwf


def calc_ShoverS_STABILITY(CLalphatail, CLalphatailless, AR, taillength, cMAC, VhoverV, Xcg, Xacwf, SM):
    STABILITYTERM = CLalphatail / CLalphatailless * (1 - calc_depsilondalpha(AR)) * taillength / cMAC * VhoverV ** 2
    ShoverSstability = 1 / STABILITYTERM * Xcg - (Xacwf - SM) / STABILITYTERM
    return ShoverSstability


AR = 8
ARh = 5
M = 0.61
eta = 0.95
halfchordsweep = 0.001  # rad approx
halfchordsweeph = 10 / 180 * np.pi  # TODO approx [rad]
b = 120
S = 2326
taperratio = 0.852
quarterchordsweep = 0  # [rad]
croot = 2 * S / ((1 + taperratio) * b)
ctip = taperratio * croot
cMAC = 19.73
cMGC = 19.73

widthfuselage = 12  # width of fuselage
heightfuselage = 12
lengthfuselage = 100  # approx length of fuselage

taillength = 50  # TODO approx
VhoverV = 0.85  # if fuselage mounted
SM = 0.05
Xacw = 0.22  # increasing shifts stability line to right, which is nice


CLalphawing = calc_CLalpha(AR, calc_beta(M), halfchordsweep)
CLalphatail = calc_CLalpha(ARh, calc_beta(M), halfchordsweeph)
CLalphatailless = CLalphawing * (1 + 2.15 * widthfuselage / b) * calc_Snet(S, croot, taperratio, b,
                                                                           widthfuselage) / S + np.pi / 2 * widthfuselage ** 2 / S
Xacwf = calc_Xacwf(Xacw, CLalphatailless, widthfuselage, heightfuselage, lengthfuselage, S, cMAC, taperratio, cMGC, b,
                   quarterchordsweep)
'''In the code the contribution of the nacelles to Xacwf is neglected as it is -0.0003 per engine'''

print('deda=', calc_depsilondalpha(AR), 'CLaw=', CLalphawing, 'CLah=', CLalphatail)
print("CLalpha A-h =", CLalphatailless)
print("Xac/c=", Xacwf)
print(1.8 / CLalphatailless * widthfuselage * heightfuselage * lengthfuselage / S / cMAC)
print('snet', calc_Snet(S, croot, taperratio, b, widthfuselage))

Xcg = np.arange(-1, 1.5, 0.05)
ShoverSstability = calc_ShoverS_STABILITY(CLalphatail, CLalphatailless, AR, taillength, cMAC, VhoverV, Xcg, Xacwf, SM)

plt.plot(Xcg, ShoverSstability)
plt.xlabel("xcg/c")
plt.ylabel("Sh/S")
plt.grid()
# plt.show()

'''From here controllability, controllability is sized for landing'''

def calc_Cmaerocwing(Cm0foil, AR, quarterchordsweep):
    Cmaerocwing = Cm0foil * (AR * np.cos(quarterchordsweep) ** 2 / (AR + 2 * np.cos(quarterchordsweep)))  # sweep assumed quarter chord sweep
    return Cmaerocwing
CLh = -0.8  # from slide 17 lecture 8
Wfin = 1879000 * 9.81
Vlanding = 77  # from boeing 787, increasing is better, 93 from A380
rho_sealevel = 1.225
CLaminush = Wfin / (0.5 * rho_sealevel * Vlanding ** 2 * S)

###'''Cmaerodynamiccentre calculation'''###
# wing
Cm0foil = -0.083

Cmaerowing = calc_Cmaerocwing(Cm0foil, AR, quarterchordsweep)
# fuselage
CL0 = CLalphawing / 180 * np.pi * 3  # CL0 is the lift coefficient of the flapped wing at zero angle of attack
Mlanding = 0.2263  # 77m/s at sealevel
betalanding = calc_beta(Mlanding)
CLalphataillessslow = calc_CLalpha(AR, betalanding, halfchordsweep)
deltafus_Cmaeroc = -1.8 * (
            1 - 2.5 * widthfuselage / lengthfuselage) * np.pi * widthfuselage * heightfuselage * lengthfuselage / (
                               4 * S * cMAC) * CL0 / CLalphataillessslow

# flaps
deltaClmax = 1.45 + 0.56  # added 0.56 for droop nose. Check for correctness
xf = 0.019 * cMAC  # 0.019 from Snorri book page 422 NACA651213
cprimeoverc = (cMAC + xf) / cMAC
deltaCLmax = 1.1 * 0.975 * 1 * 1.3  # from DATCOM 1978 eq8.4
sweephingeline = 0  # neglegible and saves a lot of time
Swf = deltaCLmax * S / (0.9 * deltaClmax * np.cos(sweephingeline))

cfoverc = 0.336
cfovercprime = cfoverc / cprimeoverc
print('cfcprime', cfovercprime)
flappedspan = 46.135 * 2
flappedspanoverb = flappedspan / b

mu1 = 0.17  # mu comes from graphs
mu2 = 0.8

CLwing = Wfin / (0.5 * rho_sealevel * Vlanding ** 2 * S)
# print('Swf=',Swf, 'flapoverb', flappedspanoverb)


deltaCmquarter = mu2 * (-mu1 * deltaClmax * cprimeoverc - (CLwing + deltaClmax * (1 - Swf / S)) / 8 * cprimeoverc * (
            cprimeoverc - 1))  # neglecting sweep term
deltaf_Cmaeroc = deltaCmquarter - CLwing * (0.25 - Xacwf)
Cmaeroc = Cmaerocwing + deltaf_Cmaeroc + deltafus_Cmaeroc  # + deltanac_Cmaeroc, neglecting nacelles for now
print('Cmac', Cmaeroc)

CONTROLLABILITYTERM = CLh / CLaminush * taillength / cMAC * VhoverV ** 2

ShoverScontrollability = 1 / CONTROLLABILITYTERM * Xcg + (Cmaeroc / CLaminush - Xacwf) / CONTROLLABILITYTERM

plt.plot(Xcg, ShoverScontrollability)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()
