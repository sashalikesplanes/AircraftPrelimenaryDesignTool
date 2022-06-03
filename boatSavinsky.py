from scipy.optimize import fsolve, minimize, Bounds, toms748, newton, brenth, brentq
import matplotlib.pyplot as plt
import numpy as np

def get_drag_at_v(V):
    b = 12 # m - beam width
    g = 9.81 # m/s2 - 
    m_total = 764e3 # mtom in kg
    VCG = 9 # m distance of CG from keel
    LCG = 30 # m from cg to end
    rho_water = 1000 # kg/m^3
    beta = 20 # deg - deadrise angle
    v_water = 0.0000010533 # m^2/s - kinematic viscosity of water
    delta_C_f = 0.0004 # standard roughness
    C_L_beta = m_total * g / (0.5 * V ** 2 * b ** 2 * rho_water)
    epsilon = 5 # deg inclination of thrust relative to keel line
    f = -6 # distance of thrust lie from cg

    def get_total_drag(tau):
        C_V = V / np.sqrt(g * b)

        C_L_0 = fsolve(lambda C_L_0 : C_L_beta + 0.0065 * beta * C_L_0 ** 0.6 - C_L_0, 1)[0]


        lambda_ = fsolve(lambda lambda_ : tau ** 1.1 * (0.012 * lambda_ ** 0.5 + 0.0055 * lambda_ ** 2.5 /  C_V ** 2) - C_L_0, 1)[0] # wetted beam length ratio
        print(f"{C_L_0 =}, {C_V=}, {tau=}, {lambda_}")

        wetted_beam_length = lambda_ * b

        V_m = V * (1 - (0.012 * lambda_ ** 0.5 * tau ** 1.1 - 0.0065 * beta * (0.012 * lambda_ ** 0.5 * tau ** 1.1) ** 0.6 / (lambda_ * np.cos(tau / 180 * np.pi)))) ** 0.5 # mean velocity over bottom surface

        R_e = V_m * lambda_ * b / v_water # Reynolds number
        C_f =  0.075 / (np.log10(R_e) - 2) ** 2 # Friction drag coefficient

        D_f = 0.5 * rho_water * V_m ** 2 * lambda_ * b ** 2 / np.cos(beta / 180 * np.pi) * (C_f + delta_C_f) # Skin friction drag


        D = m_total * g * np.tan(tau / 180 * np.pi) + D_f / np.cos(tau / 180 * np.pi)
        return D, C_V, lambda_, D_f, C_L_0

    def total_moment_f(tau):
        D, C_V, lambda_, D_f, C_L_0 = get_total_drag(tau)

        C_p = 0.75 - 1 / (5.21 * C_V ** 2 / lambda_ ** 2 + 2.39) # Center of pressure [m]

        c = LCG - C_p * lambda_ * b
        a = VCG - b / 4 * np.tan(beta / 180 * np.pi)

        M_tot = m_total * g * (c / np.cos(tau / 180 * np.pi) * (1 - np.sin(tau / 180 * np.pi) * np.sin((tau + epsilon) / 180 * np.pi)) - f * np.sin(tau / 180 * np.pi)) + D_f * (a - f)

        return M_tot

    tau_e = brentq(total_moment_f, 0.1, 20)
    results = get_total_drag(tau_e) 
    print(f"{V = }, {total_moment_f(tau_e)}")
    print(results)

    return results[0], results[1]


def main():
    velocities = np.linspace(0.1, 150, 1000)
    drags = []
    C_Vs = []
    for velocity in velocities:
        drag, C_V = get_drag_at_v(velocity)
        drags.append(drag)
        C_Vs.append(C_V)
    plt.plot(velocities, drags)
    plt.show()

if __name__ == "__main__":
    main()
