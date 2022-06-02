import matplotlib.pyplot as plt
import numpy as np

def C_L_H(V):
    if V <= 20:
        return 0.5
    elif V <= 74:
        return 0.5 / (53 ** 2) * ((V - 20) - 53)**2
    else: 
        return 0

def flapped_CL(alpha):
    C_L_alpha = 0.098
    return 2.3 - (alpha - 12) * C_L_alpha

def flapped_aoa(C_L):
    C_L_alpha = 0.098
    return 12 - (C_L - 2.3)/C_L_alpha

def funk():
    rho = 1.225
    C_L_max_flapped = 2.3 
    alpha_max_flapped = 12 # [deg]
    C_L = 1.3
    S_wing = 1770 
    g = 9.81
    Weight = 941000 * g

    rho_w = 1000
    S_H = 25

    Vs = np.arange(0, 210)
    lifts = [0.5 * 1.225 * rho * C_L * S_wing * V**2 for V in Vs]
    lifts_H = [0.5 * 1.225 * rho_w * C_L_H(V) * S_H * V**2 for V in Vs]
    lift_total = [i + j for i,j in zip(lifts, lifts_H)]
    plt.plot(Vs, lifts)
    plt.plot(Vs, lifts_H, '--')
    plt.plot(Vs, lift_total, '--')
    plt.hlines(Weight, Vs[0], Vs[-1])
    plt.show()



if __name__ == "__main__":
    funk()
