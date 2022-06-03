from scipy.optimize import fsolve
import numpy as np


V = 40 # m/s - speed
b = 12 # m - beam width
g = 9.81 # m/s2 - 
m_total = 764e3 # mtom in kg
VCG = 9 # m distance of CG from keel
LCG = 15 # m from cg to end
rho_water = 1000 # kg/m^3
C_L_beta = m_total * g / (0.5 * V ** 2 * b ** 2 * rho_water)

C_V = V / np.sqrt(g * b)
beta = 0.2 # rad - deadrise angle

C_L_0 = fsolve(lambda C_L_0 : C_L_beta + 0.0065 * beta * C_L_0 ** 0.6 - C_L_0, 1)[0]

tau = 0.1 # trim angle [rad] 

wetted_beam_length_ratio = fsolve(lambda lambda_ : tau ** 1.1 * (0.012 * lambda_ ** 0.5 + 0.0055 * lambda_ ** 2.5 /  C_V ** 2) - C_L_0, 1)[0]


wetted_beam_length = wetted_beam_length_ratio * b
print(wetted_beam_length)
