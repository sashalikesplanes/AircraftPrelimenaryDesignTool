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

def FFW(toverc):
    return 1 + 1.2*toverc + 100 * toverc**4

FFb = FFB(params["balloonFinesseRatio"])

FFw = FFW(params["thicknessOverChord"])

def Swet_balloon(volume,finesseratio):
    return 3.88 * volume**(2/3) * finesseratio **(1/3)

Swetb = Swet_balloon(params["balloonVolume"],params["balloonFinesseRatio"] )

Swetw = params['wingArea']

bw = np.sqrt(params['wingArea']*params['wingAspectRatio'])

#Sutherland's formula
#https://www.grc.nasa.gov/www/k-12/airplane/viscosity.html
visc0 = 3.62 * 10 **(-7)     #lb-s/ft2
T0_R = 518.7                 #Rankine
Delta_T = (6.5/1000) * params["altitude"]      #degree celsius
Delta_T = 1.8 * (Delta_T + 273.15)
#http://fisicaatmo.at.fcen.uba.ar/practicas/ISAweb.pdf
T = T0_R - Delta_T
visc = visc0 * ((T/T0_R)**1.5) * ((T0_R + 198.72)/(T + 198.72))

Reb = ( rho * params['velocity'] * params['balloonLength'] ) / visc

Rew = ( rho * params['velocity'] * bw ) / visc

Cfb = (1.328)/ np.sqrt(Reb)

Cfw = (1.328)/ np.sqrt(Rew)

CDF = (Cfb * FFb * Swetb ) / (params["balloonVolume"]**(2/3)) + (Cfw * FFw * Swetw ) / (params["balloonVolume"]**(2/3))

CD0 = ( CDF ) / 0.95
