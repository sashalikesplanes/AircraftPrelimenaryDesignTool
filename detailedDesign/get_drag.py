import numpy as np
#from detailedDesign.classes.Aircraft import Aircraft
#from detailedDesign.classes.Wing import Wing
from detailedDesign.classes.State import State
from misc.constants import *


def calc_viscosity(T):
    mu = 1.458e-6*T**1.5/(T+110.4)
    return mu

def calc_sflap(root_chord, taper, span, fuselage_width):
    fuselage_edge_chord = root_chord * 2 * taper / span * fuselage_width / 2
    end_of_flapped_chord = root_chord * taper * 0.7 
    flapped_area = span * (fuselage_edge_chord + end_of_flapped_chord) / 2
    return flapped_area

def calc_TO_CD_min(S_flap, S_ref):
    delta_1 = 1.016
    delta_2 = 0.0382
    delta_CD = delta_1 * delta_2 * S_flap / S_ref
    return delta_CD

def calc_reynolds(rho, V, c, T):
    Re = rho*V*c/calc_viscosity(T)
    Re_cutoff = 38.21 * (c / 0.3048 / 2.08e-5) ** 1.053
    if Re < Re_cutoff:
        return Re
    else:
        return Re_cutoff


def calc_Cf(Re, Xtroverc):
    X0overc = 36.9 * Xtroverc ** 0.625 / Re ** 0.375
    Cf = 0.074/Re**0.2*(1-(Xtroverc-X0overc))**0.8
    return Cf


def calc_CDfwing(dfus, croot, toverc, Sref, Cf):
    Sexposed = Sref - dfus * croot
    Swet = Sexposed * (1.977 + 0.52 * toverc)
    CDf = Swet/Sref*Cf
    return CDf


def calc_CDffus(Sref, cfus, dfus, Cf):
    Swet = 3.4 * cfus*dfus  # slightly overestimating
    CDf = Swet/Sref*Cf
    return CDf


def calc_CDftail(toverc, Stail, Sref, Cf):
    Swet = Stail * (1.977 + 0.52 * toverc)
    CDf = Swet/Sref*Cf
    return CDf


def calc_FFwing(toverc, M, xovercmax):
    FFwing = (1+0.6/xovercmax*toverc+100*toverc**4) * \
        1.34*M**0.18  # no compressibility or sweep
    return FFwing


def calc_FFfuselage(l, d):
    f = l/d
    FFfuselage = 1 + 60/f**3+f/400
    return FFfuselage


def calc_FFnacele(l, d):
    f = l/d
    FFnacelle = 1+0.35/f
    return FFnacelle


def calc_CDmin_wing(CDf, FFwing, IF):
    CDmin_wing = CDf*FFwing*IF['wing']
    return CDmin_wing


def calc_CDmin_fuselage(CDf, FFfuselage, IF):
    CDmin_fuselage = CDf*FFfuselage*IF['fuselage']
    return CDmin_fuselage


def calc_CDmin_tail(CDf, FFtail, IF):
    CDmin_tail = CDf*FFtail*IF['tail']
    return CDmin_tail


def calc_CDmin(CDmin_wing, CDmin_fuselage, CDmin_tail):
    CDmin = CDmin_wing + CDmin_fuselage + CDmin_tail + 0.0025  # for misc
    return CDmin


def calc_CDi(C_L, A, e):
    CDi = C_L**2/(np.pi*A*e)
    return CDi


def get_drag(aircraft):
    rho = aircraft.states['cruise'].density
    V = aircraft.states['cruise'].velocity
    cWMGC = aircraft.WingGroup.Wing.mean_geometric_chord
    T = aircraft.states['cruise'].temperature
    Sref = aircraft.reference_area
    # TODO CHECK HOW THIS WORKS FOR AN ELIPSE
    dfus = (aircraft.FuselageGroup.Fuselage.outer_height + aircraft.FuselageGroup.Fuselage.outer_height) / 2
    fuselage_width = aircraft.FuselageGroup.Fuselage.outer_height
    croot = aircraft.WingGroup.Wing.root_chord
    taper = aircraft.WingGroup.Wing.taper_ratio
    span = aircraft.WingGroup.Wing.span
    toverc = aircraft.WingGroup.Wing.thickness_chord_ratio
    xovercmax = aircraft.WingGroup.Wing.xovercmax
    M = V/aircraft.states['cruise'].speed_of_sound
    tovercVT = aircraft.FuselageGroup.Tail.VerticalTail.toverc  # from NACA0010
    tovercHT = aircraft.FuselageGroup.Tail.HorizontalTail.toverc  # from NACA0010
    xovercmaxVT = aircraft.FuselageGroup.Tail.VerticalTail.xovercmax  # from NACA0010
    xovercmaxHT = aircraft.FuselageGroup.Tail.HorizontalTail.xovercmax  # from NACA0010
    StailVT = aircraft.FuselageGroup.Tail.VerticalTail.surface_area
    StailHT = aircraft.FuselageGroup.Tail.HorizontalTail.surface_area
    cVT = aircraft.FuselageGroup.Tail.VerticalTail.mean_geometric_chord  # TODO link to vertical tail
    cHT = aircraft.FuselageGroup.Tail.HorizontalTail.mean_geometric_chord
    cfus = aircraft.FuselageGroup.Fuselage.length   # TODO link to Fuselage. (length of the fuselage)
    AR = aircraft.WingGroup.Wing.aspect_ratio     # TODO Link AR, e, CL to Wing
    V_C = aircraft.states['cruise'].velocity
    W_cruise = aircraft.mtom * 9.81
    dynamic_pressure = 0.5 * aircraft.states['cruise'].density \
        * V_C * V_C
    C_L = W_cruise / (dynamic_pressure * aircraft.WingGroup.Wing.wing_area )
    e = aircraft.WingGroup.Wing.oswald

    IF = dict({'wing': 1,  # high or mid wing
               'fuselage': 1.5,  # TODO know it is 50 % to take care of the hull, refine
               'tail': 1.04})  # conventional or T tail

    flapped_area = calc_sflap(croot, taper, span, fuselage_width):
    delta_CD_min_TO = calc_TO_CD_min(flapped_area, Sref)


    # run Wing part
    Rewing = calc_reynolds(rho, V, cWMGC, T)
    Cfwing = calc_Cf(Rewing, Xtrovercwing)
    CDfwing = calc_CDfwing(dfus, croot, toverc, Sref, Cfwing)
    FFwing = calc_FFwing(toverc, M, xovercmax)
    CDmin_wing = calc_CDmin_wing(CDfwing, FFwing, IF)

    # run fuselage part
    Refus = calc_reynolds(rho, V, cfus, T)
    Cffus = calc_Cf(Refus, Xtrovercfus)
    CDffus = calc_CDffus(Sref, cfus, dfus, Cffus)
    FFfus = calc_FFfuselage(cfus, dfus)
    CDmin_fus = calc_CDmin_fuselage(CDffus, FFfus, IF)

    # run Vtail part
    ReVT = calc_reynolds(rho, V, cVT, T)
    CfVT = calc_Cf(ReVT, Xtrovercwing)
    CDfVT = calc_CDftail(tovercVT, StailVT, Sref, CfVT)
    FFVT = calc_FFwing(tovercVT, M, xovercmaxVT)
    CDmin_VT = calc_CDmin_tail(CDfVT, FFVT, IF)

    # run Htail part
    ReHT = calc_reynolds(rho, V, cHT, T)
    CfHT = calc_Cf(ReHT, Xtrovercwing)
    CDfHT = calc_CDftail(tovercHT, StailHT, Sref, CfHT)
    FFHT = calc_FFwing(tovercHT, M, xovercmaxHT)
    CDmin_HT = calc_CDmin_tail(CDfHT, FFHT, IF)
    # test
    # add the stuff
    crud_factor = 1.25
    TotalCDmin = (CDmin_HT + CDmin_VT + CDmin_fus + \
        CDmin_wing + 0.0025) * crud_factor  # 25 DC for misc
    
    #print('FF,W-F-H-V', FFwing, FFfus, FFHT, FFVT)
    #print('CDmin, W-F-H-V', CDmin_wing, CDmin_fus, CDmin_HT, CDmin_VT)
    #print('total CDmin=', TotalCDmin)

    # hydrofoil ???
    ReHF = calc_reynolds(rho, V, 2.5, T)
    CfHF = calc_Cf(ReHF, 0.08)
    CDfHF = calc_CDftail(0.08, 25, Sref, CfHF)
    FFHF = calc_FFwing(0.08, M, .4)
    CDmin_HF = calc_CDmin_tail(CDfHF, FFHF, IF) / 1.04

    # print(f'Drag of the hydrofoil without struct: {CDmin_HF} {CDmin_HF/TotalCDmin}')

    CDi = calc_CDi(C_L, AR, e)
    CD = CDi+TotalCDmin

    CD_TO = TotalCDmin + delta_CD_min_TO + calc_CDi(aircraft.WingGroup.Wing.C_L_TO)

    #print('total CDi=', CDi)
    #print('total CD=', CDi + TotalCDmin)
    D = 0.5*rho*V**2*CD*Sref
    return TotalCDmin, CDi, CD, D, CD_TO
