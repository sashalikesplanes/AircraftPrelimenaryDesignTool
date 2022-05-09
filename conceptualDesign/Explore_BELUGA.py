import numpy as np

CR = 20
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
a = 0.5*35/2 # 60% ML radius
b = 0.5*48/2

print('altitude=',rhoair)
LbML = (0.659697-rhohelium) *V*g
LwML1 = WML-LbML
LwMLoverrho = LwML1/0.659697
LwML = LwMLoverrho*rhoair
DwML = LwML/LoverD
print('lift helium buoyancy=',LbML,'lift of wing (what we have)=',LwML, 'lift ratio B/L=', LbML/(LbML+LwML))


A = np.pi *a*b
DbBL = cdb*0.5*rhoair*v**2*A

Dtotal = DbBL + DwML
print('DbBL=',DbBL, 'dwML=', DwML, 'total=',Dtotal)

E =Dtotal*R
mfuel = E/(eta*Edens)
Vfuel = mfuel/rhohydrogen
print('mfuel=', mfuel, 'Vfuel=', Vfuel)

finenessML = 198/35
lengthBL = 2*a*finenessML

VBL = np.pi *a*b*lengthBL
print('length=',lengthBL,'radius=',a,b,'volumebeluga=',VBL)

LbBL = (rhoair-rhohydrogen)*Vfuel*g


Wpay = 500*150*g
WgrosBL = (Wpay/0.551725)*1.25 # 0.55 comes from statistical relation #TODO check the 1.25 on feasibility
LwBL = WgrosBL - LbBL
print('LwBL (needed) =',LwBL,'LbBL (what we have)=',LbBL,'WgrosBL=',WgrosBL)

print("The lift is",LwBL-LwML, " [N] to little")
