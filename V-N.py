#!/usr/bin/python3
import numpy as np

def func():
    wing_span = 136.4 
    wing_area = 2326
    MGC = 17
    W = 2119000 * 9.81
    W_min = 2119000 - 120000 - 200000
    V_stall = np.sqrt(W / (0.5 * 0.819 * 1.276 * wing_area))
    V_stall_inverted = np.sqrt(W / (0.5 * 0.819 * .35 * wing_area))
    C_L_alpha = 5.96 # [1/rad]
    C_L_max = 1.276
    C_L_min = - 0.35
    C_L_max_flaps = 1.8
    C_L_min_flaps = - 0.2
    V_H = 200
    V_C_max = 180
    print(get_n_pos(W))
    

def get_n_pos(W):
    load_factor = 2.1 + 24000 / (W + 10000)
    if load_factor <= 2.5:
        return 2.5
    elif load_factor <= 3.8:
        return load_factor
    else:
        return 3.8




if __name__ == "__main__":
    func()
