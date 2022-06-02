import numpy as np

pr = 1.3           # pressure ratio
flow_coef = 0.5     # whittle fan
omega = 2500 * 2* np.pi / 60  # rpm of the emotor from 2500 to 1800

rho =  0.8194       # kg/m3 for 4000 m
#rho = 0.259814     #A380

Ps = 61640.24       # Pa static pressure at 4000 m
#Ps = 16157.9       #A380

Tt = 350000000 # N
#Tt = 53500 * 4.44822 * 4  # from propeller sizing example
#Tt = 4 * 70000 * 4.44822 # N A380

V0 = 500 / 3.6      # m/s cruise speed
#V0 = 900/3.6    # m/s A380

P_motor = 4000000   # W
eff_mot_inv = 0.95  #

P_aircraft = Tt * V0
n_fans = np.ceil(P_aircraft/(P_motor * eff_mot_inv))

Tf = Tt/n_fans
Pt0 = Ps + 0.5 * rho * V0**2
Pt1 = Pt0 * pr
V1 = np.sqrt(2*(Pt1 - Ps) / rho)
m_dot = Tf / (V1-V0)
r = (m_dot/ (flow_coef * rho * np.pi * omega)) ** (1/3) #

# get the weight of ducted fan
D_fan = 2*r
mass_fan = 259.69*D_fan**2 + 36.954*D_fan - 1.376    # 1/3
#mass_fan = 389.54*D_fan**2 + 55.431*D_fan - 2.064  # 1/2
vol_fan = 3.3203*D_fan**2 - 3.1178*D_fan + 0.9038                # 1/3
#vol_fan = 4.9804*D_fan**2 - 4.6767*D_fan + 1.3557   # 1/2
length_fan  = vol_fan/(np.pi*r**2)

# get weight motor + inverter
#mass_motor_inverter =       # from email saluqi
specific_mass_motor_inverter = 10000  # [w/kg] from email of saluqi
mass_motor_inverter = P_motor / specific_mass_motor_inverter

# total weight of prop subsys
mass_total = n_fans * ( mass_fan + mass_motor_inverter)  #

# spacing
Span = 120
D_fus = 8.5
length_ailerons = 0.2* Span  # the aileron are 20 % of the total span
min_spacing = 0.07 * D_fan
spacing = (Span - D_fus - 2*length_ailerons -2*min_spacing - D_fan* n_fans)  / (n_fans-2)
if 0<spacing< min_spacing :
    n_fans_fit = (Span - D_fus - 2*length_ailerons)/(D_fan+min_spacing)
    print ('The engines are too close together. There are', n_fans,'fans but only', n_fans_fit, 'fit in the wing')
elif spacing<0 :
    n_fans_fit = (Span - D_fus - 2*length_ailerons )/(D_fan+min_spacing)
    print('The engines do not fit on the wing. There are', n_fans,'fans but only', n_fans_fit, 'fit in the wing')


print ('Diameter of a fan', D_fan,'m')
print ('Number of fans', n_fans)
print ('Blade tip speed', omega*r, 'm/s')
print ('Length of fan', length_fan, 'm')
print ('Total weight', mass_total*10**(-3),'Ton')
print ('Mass single fan', mass_fan,'kg')
print ('Mass motor inverter', mass_motor_inverter,'kg')
print('Spacing',spacing,'m')
