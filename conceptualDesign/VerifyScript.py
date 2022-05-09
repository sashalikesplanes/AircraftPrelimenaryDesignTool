import numpy as np
import matplotlib.pyplot as plt


#
# cd = 0.125
# rho_air = 0.412707 #kg/m3
# #T = 316000*2 #N
# S = 361.6 #m2
# eta = 0.6
# rho_E = 120 *1000000 #J/kg
# R = 10000*1000 #m
# v = 500/3.6 #m/s
#
# T = cd*0.5*rho_air*v**2*S
# P = T*v
# E = T*R
# m_fuel = E/(rho_E*eta)
#
# rho_h = 0.08988 #kg/m3
# CR = 30
# volume = m_fuel/(rho_h*CR)
#
# #print(T,m_fuel, volume,'[m3]')
#
#
# # diameter = 8.8
# slenderness = 9
# # length = 46.8
# # VV = np.pi*diameter**2*length/4
# d = np.cbrt(volume *np.pi * 4/slenderness)
# l = slenderness * d
# #print(d,l)


'''Megalifter'''

CR = 5
LoverD = 10
rhoair = 0.66
rhohelium = 0.1785
cdb = 0.05
V = 198218
g = 9.81
WML = 328854 * g
v = 500/3.6
R = 10000 *1000
eta = 0.6
Edens = 120 * 10**6
rhohydrogen = 0.08988 * CR

LbML = (0.659697-rhohelium) *V*g
LwML1 = WML-LbML
LwMLoverrho = LwML1/0.659697
LwML = LwMLoverrho*rhoair
DwML = LwML/LoverD
print('lift helium buoyancy=',LbML,'lift of wing=',LwML, 'lift ratio B/L=', LbML/(LbML+LwML))


A = np.pi * 35/2*48/2
Db = cdb*0.5*rhoair*v**2*A

Dtotal = Db + DwML
print('Db=',Db, 'dwML=', DwML, 'total=',Dtotal)

E = Dtotal * R
mfuel = E/(eta*Edens)
Vfuel = mfuel/rhohydrogen
print('mfuel=', mfuel, 'Vfuel=', Vfuel)

Wpay = 500*150*g
Wgros = (Wpay/0.551725)*1.1 # 0.55 comes from statistical relation
print('Wgros',Wgros)

Lb = (rhoair-rhohydrogen)*V*g
print('Lb',Lb)

Lw = Wgros - Lb
print('Lw',Lw)