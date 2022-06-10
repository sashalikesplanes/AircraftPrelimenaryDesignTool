import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

from misc.ISA import getPressure
from detailedDesign.calculate_stress import calculate_stress
from detailedDesign.section_design import plate_crippling


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
    df_location = Path('data', 'dataframes', 'fuselage_stresses_t_5.dat')

    # force_run = True
    try:
        if force_run:
            raise FileNotFoundError
        df = pd.read_csv(df_location)
    except FileNotFoundError:
        # for t in np.arange(0.001, 0.010, 0.001):
        for t in [0.0045]:
            # t = 0.005
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
            t_mm = int(round(t * 1000))
            df_location2 = Path('data', 'dataframes', f'fuselage_stresses_t_{t_mm}.dat')
            df.to_csv(df_location2)

    df["stress_max"] = df[["stress_1", "stress_2"]].abs().max(axis=1)

    max_abs_shear = max(df["stress_max"])
    shear_cut1 = max_abs_shear / 3
    shear_cut2 = max_abs_shear * 2 / 3

    conditions = [
        (df["stress_max"] <= shear_cut1),
        (df["stress_max"] > shear_cut1) & (df["stress_max"] <= shear_cut2),
        (df["stress_max"] > shear_cut2)
    ]
    values = ["heavy", "medium", "light"]
    df['section_type'] = np.select(conditions, values)
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

    ax.set_xlim3d(0, 120)
    ax.set_ylim3d(-10, 10)
    ax.set_zlim3d(-10, 10)
    print(f"Maximum stress: {10 ** -6 * max(df['stress_1'])} [MPa], Minimum stress: {10 ** -6 * min(df['stress_2'])} [MPa]")
    ax.scatter(df["x"], df["y"], df["z"], c=df["stress_max"], lw=0, s=20)
    plt.show()

    plate_crippling(0.0045, aircraft)


