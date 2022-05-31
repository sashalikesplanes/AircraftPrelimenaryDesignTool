# Stability
import numpy as np
import matplotlib.pyplot as plt




def calc_Snet(S, croot, taperratio, b, widthfuselage):
    Snet = S - croot * (1 + taperratio + (
            b - widthfuselage) / b) * widthfuselage / 2  # Surface area wing - area inside the fuselage
    return Snet


def calc_CLalpha(aspect_ratio, beta, semi_chord_sweep, eta):
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

'''control'''
def calc_Cmaerocwing(Cm0foil, AR, quarterchordsweep):
    Cmaerocwing = Cm0foil * (AR * np.cos(quarterchordsweep) ** 2 / (AR + 2 * np.cos(quarterchordsweep)))  # sweep assumed quarter chord sweep
    return Cmaerocwing


def calc_deltafus_Cmaeroc(widthfuselage, lengthfuselage, heightfuselage, cMAC, CL0, CLalphataillessslow, S):
    deltafus_Cmaeroc = -1.8 * (1 - 2.5 * widthfuselage / lengthfuselage) * np.pi * widthfuselage * heightfuselage * lengthfuselage / (
                               4 * S * cMAC) * CL0 / CLalphataillessslow
    return deltafus_Cmaeroc


def calc_deltaflap_Cmaeroc(cMAC, CLwing, deltaCLmax, sweephingeline, S, Xacwf):
    deltaClmax = 1.45 + 0.56  # added 0.56 for droop nose. Check for correctness
    mu1 = 0.17  # mu comes from graphs
    mu2 = 0.8
    xf = 0.019 * cMAC  # 0.019 from Snorri book page 422 NACA651213
    Swf = deltaCLmax * S / (0.9 * deltaClmax * np.cos(sweephingeline))
    cprimeoverc = (cMAC + xf) / cMAC
    deltaCmquarter = mu2 * (-mu1 * deltaClmax * cprimeoverc - (CLwing + deltaClmax * (1 - Swf / S)) / 8 * cprimeoverc * (cprimeoverc - 1))  # neglecting sweep term
    deltaflap_Cmaeroc = deltaCmquarter - CLwing * (0.25 - Xacwf)
    return deltaflap_Cmaeroc


def calc_ShoverScontrollability(CLh, CLaminush, taillength, cMAC, VhoverV, Xcg, Cmaeroc, Xacwf):
    CONTROLLABILITYTERM = CLh / CLaminush * taillength / cMAC * VhoverV ** 2
    ShoverScontrollability = 1 / CONTROLLABILITYTERM * Xcg + (Cmaeroc / CLaminush - Xacwf) / CONTROLLABILITYTERM
    return ShoverScontrollability


def get_xplot(aircraft):
    AR = aircraft.WingGroup.Wing.aspect_ratio
    ARh = aircraft.FuselageGroup.Tail.HorizontalTail.aspect_ratio
    M = aircraft.states['cruise'].velocity/aircraft.states['cruise'].speed_of_sound
    Vlanding = 77  # from boeing 787, increasing is better, 93 from A380
    Mlanding = 0.2263  # 77m/s at sealevel

    eta = 0.95  # from Sam

    b = aircraft.WingGroup.Wing.span
    S = aircraft.WingGroup.Wing.wing_area
    taperratio = aircraft.WingGroup.Wing.taper_ratio
    quarterchordsweep = aircraft.WingGroup.Wing.sweep  # [rad]
    croot = 2 * S / ((1 + taperratio) * b)
    ctip = taperratio * croot
    cMGC = aircraft.WingGroup.Wing.mean_geometric_chord
    cMAC = cMGC*1
    halfchordsweep = np.arctan(np.tan(quarterchordsweep)-4/AR*(0.5-0.25*(1-taperratio)/(1+taperratio)))  # rad approx from eq9-11 snorri
    quarterchordsweeph = aircraft.FuselageGroup.Tail.HorizontalTail.quarter_chord_sweep
    halfchordsweeph = np.arctan(np.tan(quarterchordsweeph)-4/AR*(0.5-0.25*(1-taperratio)/(1+taperratio)))



    widthfuselage = aircraft.FuselageGroup.Fuselage.diameter  # At this stage the same due to circular
    heightfuselage = aircraft.FuselageGroup.Fuselage.diameter
    lengthfuselage = aircraft.FuselageGroup.Fuselage.length

    taillength = aircraft.FuselageGroup.Tail.HorizontalTail.tail_length
    VhoverV = 0.85  # if fuselage mounted
    SM = 0.05 # as defined in ADSEE
    Xacw = 0.23  # increasing shifts stability line to right, which is nice
    Xacwlanding = 0.24  #TODO, check for final landing, slide 31, adsee3PPT7

    CLh = -0.8  # from slide 17 lecture 8
    Wfin = aircraft.mtom - aircraft.fuel_mass # TODO check for reserve fuel
    rho_sealevel = 1.225
    CLaminush = Wfin / (0.5 * rho_sealevel * Vlanding ** 2 * S) - CLh

    CLalphawing = calc_CLalpha(AR, calc_beta(M), halfchordsweep, eta)
    CLalphawinglanding = calc_CLalpha(AR, calc_beta(Mlanding), halfchordsweep, eta)
    CLalphatail = calc_CLalpha(ARh, calc_beta(M), halfchordsweeph, eta)
    #CLalphataillanding = calc_CLalpha(ARh, calc_beta(Mlanding), halfchordsweeph, eta)

    CLalphatailless = CLalphawing * (1 + 2.15 * widthfuselage / b) * calc_Snet(S, croot, taperratio, b,
                                                                               widthfuselage) / S + np.pi / 2 * widthfuselage ** 2 / S
    CLalphataillesslanding = CLalphawinglanding * (1 + 2.15 * widthfuselage / b) * calc_Snet(S, croot, taperratio, b,
                                                                                             widthfuselage) / S + np.pi / 2 * widthfuselage ** 2 / S
    Xacwf = calc_Xacwf(Xacw, CLalphatailless, widthfuselage, heightfuselage, lengthfuselage, S, cMAC, taperratio, cMGC,
                       b,quarterchordsweep)
    Xacwflanding = calc_Xacwf(Xacwlanding, CLalphataillesslanding, widthfuselage, heightfuselage, lengthfuselage, S, cMAC, taperratio, cMGC,
                       b, quarterchordsweep)

    Xcg = np.arange(-1, 1.5, 0.05)
    ShoverSstability = calc_ShoverS_STABILITY(CLalphatail, CLalphatailless, AR, taillength, cMAC, VhoverV, Xcg, Xacwf, SM)

    ###'''Cmaerodynamiccentre calculation'''###
    # wing
    Cm0foil = -0.083  # alpha = 0, cm from NACA 651412
    Cmaerocwing = calc_Cmaerocwing(Cm0foil, AR, quarterchordsweep)

    # fuselage
    CL0 = CLalphawing / 180 * np.pi * 3  # CL0 is the lift coefficient of the flapped wing at zero angle of attack
    deltafus_Cmaeroc = calc_deltafus_Cmaeroc(widthfuselage, lengthfuselage, heightfuselage, cMAC, CL0,
                                             CLalphataillesslanding, S)

    # flaps
    deltaCLmax = 1.1 * 0.975 * 1 * 1.3  # from DATCOM 1978 eq8.4
    sweephingeline = 0  # neglegible and saves a lot of time
    CLwing = Wfin / (0.5 * rho_sealevel * Vlanding ** 2 * S)  # all flaps must be deployed
    deltaflap_Cmaeroc = calc_deltaflap_Cmaeroc(cMAC, CLwing, deltaCLmax, sweephingeline, S, Xacwflanding)
    Cmaeroc = Cmaerocwing + deltaflap_Cmaeroc + deltafus_Cmaeroc  # + deltanac_Cmaeroc, neglecting nacelles for now, and no formulas for it
    #print('Cmac', Cmaeroc)

    ShoverScontrollability = calc_ShoverScontrollability(CLh, CLaminush, taillength, cMAC, VhoverV, Xcg, Cmaeroc, Xacwf)



    plt.plot(Xcg, ShoverSstability)
    plt.plot(Xcg, ShoverScontrollability)
    plt.xlabel("xcg/c")
    plt.ylabel("Sh/S")
    plt.grid()
    plt.xlim(-0.5, 1)
    plt.ylim(0, 1)
    plt.title("X-plot")
    plt.show()
    return





# '''In the code the contribution of the nacelles to Xacwf is neglected as it is -0.0003 per engine'''
# Controllability is sized for landing
# '''formulas to get the constants'''
# xf = 0.019 * cMAC  # 0.019 from Snorri book page 422 NACA651213
# cprimeoverc = (cMAC + xf) / cMAC
# cfoverc = 0.336
# cfovercprime = cfoverc / cprimeoverc
# print('cfcprime', cfovercprime)
# flappedspan = 46.135 * 2  # 46.135 comes from trapezoidal relation, gives a nonlinear system of equations
# flappedspanoverb = flappedspan / b





