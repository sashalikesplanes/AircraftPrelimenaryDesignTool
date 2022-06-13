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
    fuselage_bending_shear(aircraft, force_run)
    wing_bending_shear(aircraft, force_run)


def wing_bending_shear(aircraft, force_run):
    # Open the dataframe containing the wing loading data if it is present
    df_location = Path('data', 'dataframes', 'wing_loading.dat')
    try:
        if force_run:
            raise FileNotFoundError
        df = pd.read_csv(df_location)
    except FileNotFoundError:
        data_started = False
        data = []

        location = Path('data', 'xflr5', 'xflr_file_1.txt')
        with open(location) as file:
            for line in file.readlines():
                line = line.strip("\n")
                if line == "Main Wing":
                    data_started = True
                elif data_started:
                    line = line.split(" ")

                    line = [x for x in line if x != '']
                    if len(line) > 0:
                        data.append(line)

        header = data.pop(0)
        data = np.array([[float(y) for y in x] for x in data])
        df = pd.DataFrame(data, columns=header)
        df.to_csv(df_location, index=False)

    # Start analysis
    print(df)


def fuselage_bending_shear(aircraft, force_run):
    # if (self.FuselageGroup.Fuselage.outer_height == self.FuselageGroup.Fuselage.outer_width):
    #     I_zz = np.pi/64*(self.FuselageGroup.Fuselage.outer_width**4-self.FuselageGroup.Fuselage.inner_width**4)
    #     I_yy = I_zz
    # else:

    # retrieve the principal lengths for the ellipse
    b = aircraft.FuselageGroup.Fuselage.outer_height
    a = aircraft.FuselageGroup.Fuselage.outer_width

    # Start 3D fuselage stress plot
    df_location = Path('data', 'dataframes', 'fuselage_stresses_t_1.dat')

    try:
        # Open the file if present or raise a FileNotFoundError if the file needs to be remade either way
        if force_run:
            raise FileNotFoundError
        df = pd.read_csv(df_location)
    except FileNotFoundError:
        # for t in np.arange(0.001, 0.010, 0.001):
        for t in [0.001]:
            # t = 0.005
            header = ["x", "y", "z", "stress_1", "stress_2"]
            data_x = []
            data_y = []
            data_z = []
            data_stress = []

            for x in tqdm(range(len(aircraft.FuselageGroup.Fuselage.longitudinal_moment))):
                for theta in np.arange(0, 2 * np.pi, 0.25):
                    y = a / 2 * cos(theta)
                    z = b / 2 * sin(theta)
                    data_stress.append(calculate_stress(x, y, z, t, aircraft))
                    data_x.append(x * 0.1)
                    data_y.append(y)
                    data_z.append(z)

            data = np.transpose(
                np.array([data_x, data_y, data_z, [x[0] for x in data_stress], [x[1] for x in data_stress]]))
            df = pd.DataFrame(data, columns=header)
            df.to_csv(df_location, index=False)
            t_mm = int(round(t * 1000))
            df_location2 = Path('data', 'dataframes', f'fuselage_stresses_t_{t_mm}.dat')
            df.to_csv(df_location2, index=False)

    # Find the maximum stress from the two principal stresses
    df["stress_max"] = df[["stress_1", "stress_2"]].abs().max(axis=1)

    # Find the maximum shear and the shears for the lighter sections
    max_abs_shear = max(df["stress_max"])
    shear_cut1 = max_abs_shear / 3
    shear_cut2 = max_abs_shear * 2 / 3

    conditions = [
        (df["stress_max"] <= shear_cut1),
        (df["stress_max"] > shear_cut1) & (df["stress_max"] <= shear_cut2),
        (df["stress_max"] > shear_cut2)
    ]
    values = ["light", "medium", "heavy"]
    df['section_type'] = np.select(conditions, values)

    # # Old plot which makes a polar plot for the stresses at one segment
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

    # Make a 3D plot for the stresses present in the fuselage
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(0, 120)
    ax.set_ylim3d(-10, 10)
    ax.set_zlim3d(-10, 10)
    print(
        f"Maximum stress: {10 ** -6 * max(df['stress_1'].abs())} [MPa], Minimum stress: {10 ** -6 * max(df['stress_2'].abs())} [MPa]")
    ax.scatter(df["x"], df["y"], df["z"], c=df["stress_max"], lw=0, s=20)
    plt.show()

    # Make a list of the cuts for the different segments
    segment_stresses = [max_abs_shear, shear_cut2, shear_cut1]

    # Find the stress the material can handle after enduring fatigue cycles (Al-7075)
    sigma_fatique = 159e6

    # Find the different segment skin thicknesses based on the known stress at t = 1 mm
    segment_thicknesses = [np.ceil(x / sigma_fatique) for x in segment_stresses]

    # Conditions for the next columns which will be added
    conditions = [
        (df["section_type"] == "heavy"),
        (df["section_type"] == "medium"),
        (df["section_type"] == "light")
    ]

    # Add the thickness and the crippling stress to the different columns of the dataframe
    df['thickness'] = np.select(conditions, segment_thicknesses)
    segment_buckling = [plate_crippling(x, aircraft) for x in segment_thicknesses]
    df['buckling_stress'] = np.select(conditions, segment_buckling)

    # Find the maximum thickness per fuselage slice
    max_thickness = df.groupby("x").thickness.transform(max)

    # Plot the fuselage thickness against longitudinal position
    plt.figure()
    plt.plot(df["x"], max_thickness)
    plt.title("Longitudinal Skin Thickness Variation")
    plt.xlabel("Longitudinal position [m]")
    plt.ylabel("Skin Thickness [mm]")

    # Save the final dataframe with all the additional columns
    df_location2 = Path('data', 'dataframes', f'fuselage_stresses_final.dat')
    df.to_csv(df_location2, index=False)
