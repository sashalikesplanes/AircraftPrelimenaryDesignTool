import numpy as np


def dragModel(params, rho):
    wingDrag = 0.5 * rho * params['velocity'] ** 2 * \
        (params['wingArea'] * params['wingC_D'])

    balloonDrag = 0.5 * rho * params['velocity'] ** 2 * \
        (params['balloonVolume'] ** (2/3) * params['balloonC_D'])
    fuselageDrag = 0.5 * rho * \
        params['velocity'] ** 2 * \
        (params['fuselageArea'] * params['fuselageC_D'])
    fuselageDrag = 0
    params['totalDrag'] = wingDrag + balloonDrag + fuselageDrag


def FFB(finesseratio):
    return 1 + 1.5/(finesseratio**(2/3)) + 7/(finesseratio**(3))

def FFW(tOverC):
    return 1 + 1.2*tOverC + 100 * tOverC**4


def Swet_balloon(volume,finesseratio):
    return 3.88 * volume**(2/3) * finesseratio **(1/3)

def get_visc(altitude):
    #Sutherland's formula
    #https://www.grc.nasa.gov/www/k-12/airplane/viscosity.html
    visc0 = 1.716e-5      #lb-s/ft2
    T0_R = 273                 #Rankine
    Delta_T = (6.5/1000) * altitude      #degree celsius
    #http://fisicaatmo.at.fcen.uba.ar/practicas/ISAweb.pdf
    T = T0_R - Delta_T
    visc = visc0 * ((T/T0_R)**1.5) * ((T0_R + 111)/(T + 111))
    return visc



def get_CD_0(params, rho):
    FFb = FFB(params["balloonFinesseRatio"])
    print(f'{FFb = }')

    FFw = FFW(params["thicknessOverChord"])
    print(f'{FFw = }')

    Swetb = Swet_balloon(params["balloonVolume"],params["balloonFinesseRatio"] )
    print(f'{Swetb = }')

    Swetw = 2 * params['wingArea']
    print(f'{Swetw = }')

    bw = np.sqrt(params['wingArea']*params['wingAspectRatio'])
    print(f'{bw = }')

    visc = get_visc(params["altitude"])
    print(f'{visc = }')

    Reb = ( rho * params['velocity'] * params['balloonLength'] ) / visc
    print(f'{Reb = }')

    Rew = ( rho * params['velocity'] * bw ) / visc
    print(f'{FFb = }')

    Cfb = 0.455/(np.log10(Reb)**2.58)
    print(f'{Cfb = }')

    Cfw = 0.455/(np.log10(Rew)**2.58)

    print(f'{Cfw = }')

    CDF = (Cfb * FFb * Swetb ) / (params["balloonVolume"]**(2/3)) + (Cfw * FFw * Swetw ) / (params["balloonVolume"]**(2/3))
    print(f'{CDF = }')

    CD_0 = ( CDF ) / 0.95
    return CD_0







if __name__ == "__main__":
    parameters = openData("design1")

    run_concept(parameters)
    main()
