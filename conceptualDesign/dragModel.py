import numpy as np
from conceptualDesign.sweepAngles import convertSweep


def dragModel(params, rho, temp):
    """ Main function called by outside modules"""
    # Establish Drag Coefficient [-]
    # Calculate the corresponding drag in [N]

    C_D = get_drag(params, rho, temp)
    D = 0.5 * rho * params['velocity'] ** 2 * \
            C_D * params['wingArea']

    params['totalDrag'] = D * params["dragContingency"]


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



def airplane_design_drag_components(params, rho, temp, viscosity):
    specificGasConstantAir = 287.058
    machNumber = params['velocity'] / \
        np.sqrt(1.4 * specificGasConstantAir * temp)
    # Form Factor
    wingFF = estimate_wing_FF(params, params['maxThicknessLocationAirfoil'],
                              params['thicknessOverChord'], machNumber)
    fuselageFF = estimate_fuselage_FF(params['fuselageLength'],
                                      2 * params['fuselageRadius'])
    # Wetted Area
    wingS_wet = get_wetted_area_wing(params["thicknessOverChord"],
                                     params["wingArea"])
    fuselageS_wet = get_wetted_area_fuselage(params['fuselageLength'],
                                             2 * params['fuselageRadius'])
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


def get_C_D_0(params, rho, temp):
    airViscosity = get_viscosity(params["altitude"])
    C_D_0 = airplane_design_drag_components(
            params, rho, temp, airViscosity)
    return C_D_0


def estimate_CL_alpha(aspectRatio, sweep=0):
    return 2 * np.pi * aspectRatio / (2 + np.sqrt(4 + aspectRatio * aspectRatio *
                                                  (1 + np.tan(sweep)**2)))


def determine_balloon_ar(volume, width):
    return width * width / (2 * volume ** (2 / 3))


def get_CD_i(params):
    wingC_L = params['wingC_L_design']
    oswaldFactor = get_oswald_efficiency(params['wingAspectRatio'],
                                         convertSweep(params['wingQuarterChordSweep'],
                                                      0,
                                                      params['wingTaperRatio'],
                                                      params['wingAspectRatio']))
    wingC_D_i = wingC_L**2 / (np.pi * params['wingAspectRatio'] * 0.8)
    return  wingC_D_i


def get_drag(params, rho, temp):
    return get_C_D_0(params, rho, temp) + get_CD_i(params)
