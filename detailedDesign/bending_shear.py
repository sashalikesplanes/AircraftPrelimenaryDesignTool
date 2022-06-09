import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

from misc.ISA import getPressure


cos = np.cos
sin = np.sin


def find_bending_shear(aircraft, force_run=False):
    fuselage = aircraft.FuselageGroup.Fuselage
    # if (self.FuselageGroup.Fuselage.outer_height == self.FuselageGroup.Fuselage.outer_width):
    #     I_zz = np.pi/64*(self.FuselageGroup.Fuselage.outer_width**4-self.FuselageGroup.Fuselage.inner_width**4)
    #     I_yy = I_zz
    # else:

    # Initialisation
    # z = np.linspace(0, z_max, 100)
    # y = np.linspace(0, y_max, 100)
    t = np.linspace(0, 0.5, 100)

    # retrieve the principal lengths for the ellipse
    b = aircraft.FuselageGroup.Fuselage.outer_height
    a = aircraft.FuselageGroup.Fuselage.outer_width

    # Start 3D fuselage stress plot
    df_location = Path('data', 'dataframes', 'fuselage_stresses.dat')

    force_run = True
    try:
        if force_run:
            raise FileNotFoundError
        df = pd.read_csv(df_location)
    except FileNotFoundError:
        t = 0.005
        header = ["x", "y", "z", "stress_1", "stress_2"]
        data_x = []
        data_y = []
        data_z = []
        data_stress = []

        for x in tqdm(range(len(aircraft.FuselageGroup.Fuselage.longitudinal_moment))):
            for theta in np.arange(0, 2 * np.pi, 0.025):
                y = a / 2 * cos(theta)
                z = b / 2 * sin(theta)
                data_stress.append(calculate_stress(x, y, z, t, aircraft))
                data_x.append(x * 0.1)
                data_y.append(y)
                data_z.append(z)

        data = np.transpose(np.array([data_x, data_y, data_z, [x[0] for x in data_stress], [x[1] for x in data_stress]]))
        df = pd.DataFrame(data, columns=header)
        df.to_csv(df_location)

    print(df)

    # sigma_1 = np.array([x[0] for x in data_stress]) * 10 ** -6  # [MPa]
    # sigma_2 = np.array([x[1] for x in data_stress]) * 10 ** -6  # [MPa]
    #
    # plt.figure()
    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    # x_values = list(np.arange(0, 2 * np.pi, 0.1))
    # ax.plot(x_values + x_values[:1], list(sigma_1) + list(sigma_1)[:1])
    # ax.plot(x_values + x_values[:1], list(sigma_2) + list(sigma_2)[:1])
    # ax.set_title("Stress over rotation")
    # # plt.xlabel("Rotation around axis [rad]")
    # # plt.ylabel("Stress [MPa]")
    # # ax.set(xlabel="Rotation around axis [rad]", ylabel="Stress [MPa]")
    # ax.grid(True)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(df["x"], df["y"], df["z"], c=df["stress_1"], lw=0, s=20)
    plt.show()



def calculate_stress(x, y, z, t, aircraft):
    # Base the radius on the y and z coordinates of the point
    r = (y ** 2 + z ** 2) ** 0.5

    S_y = -aircraft.FuselageGroup.Tail.VerticalTail.F_w
    S_z = aircraft.FuselageGroup.Fuselage.longitudinal_shear[x]
    M_z = (aircraft.FuselageGroup.Fuselage.Cabin.length - aircraft.FuselageGroup.Aircraft.get_cg()[0]) * S_y
    M_y = aircraft.FuselageGroup.Fuselage.longitudinal_moment[x]
    T = S_y * (aircraft.FuselageGroup.Tail.VerticalTail.span / 2)

    # first moment of area
    a = aircraft.FuselageGroup.Fuselage.outer_height
    b = aircraft.FuselageGroup.Fuselage.outer_width

    Q_z = 4 * b ** 2 * a / 3 - (4 * (b - 2 * t) ** 2 * (a - 2 * t) / 3)
    Q_y = 4 * a ** 2 * b / 3 - (4 * (a - 2 * t) ** 2 * (b - 2 * t) / 3)

    I_yy = np.pi / 64 * (a ** 3 * b - (a - 2 * t) ** 3 * (b - 2 * t))
    I_zz = np.pi / 64 * (b ** 3 * a - (b - 2 * t) ** 3 * (a - 2 * t))
    delta_P = np.abs(getPressure(aircraft.FuselageGroup.Aircraft.states['cruise'].altitude) - getPressure(
        aircraft.FuselageGroup.Fuselage.Cabin.cabin_pressure_altitude))
    J_0 = I_yy + I_zz

    # Calculate stresses
    sigma_x = M_z * y / I_zz + M_y * z / I_yy + delta_P * r / t
    sigma_y = 2 * r * delta_P / t

    shear = -(S_y * Q_z) / (I_zz * t) - (S_z * Q_y) / (I_yy * t) + T * r / J_0

    tau_max = (((sigma_x - sigma_y) / 2)**2 + shear ** 2) ** 0.5

    sigma_1 = (sigma_x + sigma_y) / 2 + tau_max
    sigma_2 = (sigma_x + sigma_y) / 2 - tau_max
    result = (sigma_x, sigma_y)
    # print(result, shear)
    return result
