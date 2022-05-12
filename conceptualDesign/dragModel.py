import numpy as np
from conceptualDesign.sweepAngles import convertSweep


def dragModel(params, rho, temp):
    """ Main function called by outside modules"""
    # Establish Drag Coefficient [-]
    # Calculate the corresponding drag in [N]

    designConcept = params["designConcept"]
    C_D = get_drag(params, rho, temp, designConcept)
    # print(f"{C_D}")
    if designConcept <= 3:  # Concepts with a balloon
        D = 0.5 * rho * params['velocity'] ** 2 * \
            C_D * params['balloonVolume'] ** (2 / 3)
    elif designConcept == 4:  # Concept without a balloon
        D = 0.5 * rho * params['velocity'] ** 2 * \
            C_D * params['wingArea']

    params['totalDrag'] = abs(D) * params["dragContingency"]
    # print(D)


def FFB(finesseratio):
    return 1 + 1.5 / (finesseratio**(2/3)) + 7 / (finesseratio**(3))


def FFW(tOverC):
    return 1 + 1.2 * tOverC + 100 * tOverC ** 4


def Swet_balloon(volume, finesseratio):
    return 3.88 * volume**(2/3) * finesseratio ** (1/3)


def get_viscosity(altitude):
    # Sutherland's formula
    # https://www.grc.nasa.gov/www/k-12/airplane/viscosity.html
    visc0 = 1.716e-5
    T0_R = 273
    Delta_T = (6.5 / 1000) * altitude  # degree celsius
    # http://fisicaatmo.at.fcen.uba.ar/practicas/ISAweb.pdf
    T = T0_R - Delta_T
    visc = visc0 * ((T / T0_R) ** 1.5) * ((T0_R + 111) / (T + 111))
    return visc


def get_wetted_area_wing(tOverC, referenceArea):
    return referenceArea * (1.977 + 0.52 * tOverC)


def get_wetted_area_fuselage(fuselageLength, fuselageRadius):
    return 3.4 * fuselageRadius * fuselageLength


def get_oswald_efficiency(aspectRatio, leadingEdgeSweep):
    if leadingEdgeSweep <= np.deg2rad(30):  # degree
        return 1.78 * (1 - 0.045 * aspectRatio ** 0.68) - 0.64
    else:
        return 4.61 * (1 - 0.045 * aspectRatio ** 0.68) * (np.cos(leadingEdgeSweep) ** 0.15) - 3.1


def estimate_wing_FF(params, maxThicknessLocationAirfoil, tOverC, machNumber):
    maxThicknessSweep = convertSweep(params['wingQuarterChordSweep'],
                                     maxThicknessLocationAirfoil,
                                     params['wingTaperRatio'],
                                     params['wingAspectRatio'])
    return (1 + 0.6 / maxThicknessLocationAirfoil * tOverC + 100 * tOverC ** 4) * \
           (1.34 * machNumber ** 0.18 * np.cos(maxThicknessSweep) ** 0.28)


def estimate_fuselage_FF(fuselageLength, fuselageRadius):
    fFactor = fuselageLength / fuselageRadius
    return 1 + 60 / (fFactor ** 3) + fFactor / 400


def balloon_design_drag_components(params, rho, viscosity):
    # Form Factor
    balloonFF = FFB(params["balloonFinesseRatio"])
    wingFF = FFW(params["thicknessOverChord"])
    # Wetted Area
    balloonS_wet = Swet_balloon(
        params["balloonVolume"], params["balloonFinesseRatio"])
    wingS_wet = get_wetted_area_wing(
        params['thicknessOverChord'], params['wingArea'])
    # Reynolds Number
    balloonRe = (rho * params['velocity'] *
                 params['balloonLength']) / viscosity
    wingRe = (rho * params['velocity'] *
              params['meanAerodynamicChord']) / viscosity
    # Skin Friction
    balloonC_f = 0.455 / (np.log10(balloonRe) ** 2.58)
    wingC_f = 0.455 / (np.log10(wingRe) ** 2.58)
    C_D_F = ((balloonC_f * balloonFF * balloonS_wet) + (wingC_f * wingFF * wingS_wet)) / \
            (params["balloonVolume"]**(2/3))
    return (C_D_F) / 0.95


def airplane_design_drag_components(params, rho, temp, viscosity):
    specificGasConstantAir = 287.058
    machNumber = params['velocity'] / \
        np.sqrt(1.4 * specificGasConstantAir * temp)
    # print(f'{machNumber = }')
    # Form Factor
    wingFF = estimate_wing_FF(params, params['maxThicknessLocationAirfoil'],
                              params['thicknessOverChord'], machNumber)
    # print(f'{wingFF = }')
    fuselageFF = estimate_fuselage_FF(params['fuselageLength'],
                                      2 * params['fuselageRadius'])
    # print(f'{fuselageFF = }')
    # Wetted Area
    wingS_wet = get_wetted_area_wing(params["thicknessOverChord"],
                                     params["wingArea"])
    # print(f'{wingS_wet = }')
    fuselageS_wet = get_wetted_area_fuselage(params['fuselageLength'],
                                             2 * params['fuselageRadius'])
    # print(f'{fuselageS_wet = }')

    # Reynolds Number
    wingRe = rho * params['velocity'] * \
        params['meanAerodynamicChord'] / viscosity
    wingRe_cutoff = 38.21 * \
        (params['meanAerodynamicChord'] / (2.08e-5 * .3048))**1.053
    fuselageRe = rho * params['velocity'] * \
        params['fuselageLength'] / viscosity
    fuselageRe_cutoff = 38.21 * \
        (params['fuselageLength'] / (2.08e-5 * .3048))**1.053
    # Skin Friction
    wingC_f = 0.455 / (np.log10(min(wingRe, wingRe_cutoff))**2.58
                       * (1 + 0.144 * machNumber ** 2) ** 0.65)
    # print(f'{wingC_f = }')
    fuselageC_f = 0.455 / (np.log10(min(fuselageRe, fuselageRe_cutoff))**2.58
                           * (1 + 0.144 * machNumber ** 2) ** 0.65)
    # print(f'{fuselageC_f = }')
    return ((wingC_f*wingFF*wingS_wet) + (fuselageC_f*fuselageFF*fuselageS_wet)) / \
        params['wingArea']


def get_C_D_0(params, rho, temp, designConcept):
    airViscosity = get_viscosity(params["altitude"])
    if designConcept <= 3:
        C_D_0 = balloon_design_drag_components(params, rho, airViscosity)
    elif designConcept == 4:
        C_D_0 = airplane_design_drag_components(
            params, rho, temp, airViscosity)
    # print(f'{designConcept}')
    # print(f'{C_D_0}')
    return C_D_0


def estimate_CL_alpha(aspectRatio, sweep=0):
    return 2 * np.pi * aspectRatio / (2 + np.sqrt(4 + aspectRatio * aspectRatio *
                                                  (1 + np.tan(sweep)**2)))


def estimate_K_factor(aspectRatio):
    return -0.0145 * (aspectRatio) ** (-4) + 0.182 * (aspectRatio) ** (-3) - \
        0.514 * (aspectRatio) ** (-2) + 0.838 * (1 / aspectRatio) - 0.053


def determine_balloon_ar(volume, width):
    return width * width / (2 * volume ** (2 / 3))


def get_CD_i(params):
    balloonAr = determine_balloon_ar(
        params['balloonVolume'], params['balloonRadius']*2)
    balloonAoA = np.deg2rad(2)  # deg ## TODO:::implemet AoA optimization
    balloonC_L = balloonAoA * estimate_CL_alpha(balloonAr)
    wingC_L = params['wingC_L_design']
    kFactor = estimate_K_factor(balloonAr)
    balloonC_D_i = kFactor * balloonC_L ** 2
    conversionRatioWingDrag = params['wingArea'] / \
        (params['balloonVolume'] ** (2/3))
    oswaldFactor = get_oswald_efficiency(params['wingAspectRatio'],
                                         convertSweep(params['wingQuarterChordSweep'],
                                                      0,
                                                      params['wingTaperRatio'],
                                                      params['wingAspectRatio']))
    # print(f'{oswaldFactor = }')
    wingC_D_i = wingC_L**2 / (np.pi * params['wingAspectRatio'] * oswaldFactor) *\
        conversionRatioWingDrag
    # print(f'{balloonC_D_i + wingC_D_i}')
    return balloonC_D_i + wingC_D_i


def get_drag(params, rho, temp, designConcept):
    return get_C_D_0(params, rho, temp, designConcept) + get_CD_i(params)
