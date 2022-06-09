import numpy as np
import matplotlib.pyplot as plt

from misc.ISA import getPressure


def find_bending_shear(aircraft):
    fuselage = aircraft.FuselageGroup.Fuselage
    # if (self.FuselageGroup.Fuselage.outer_height == self.FuselageGroup.Fuselage.outer_width):
    #     I_zz = np.pi/64*(self.FuselageGroup.Fuselage.outer_width**4-self.FuselageGroup.Fuselage.inner_width**4)
    #     I_yy = I_zz
    # else:

    # Initialisation
    # z = np.linspace(0, z_max, 100)
    # y = np.linspace(0, y_max, 100)
    t = np.linspace(0, 0.5, 100)
    # t = max(self.FuselageGroup.Fuselage.outer_height/2 - self.FuselageGroup.Fuselage.inner_height/2, self.FuselageGroup.Fuselage.outer_width/2 - self.FuselageGroup.Fuselage.inner_width/2)

    z_max = fuselage.FuselageGroup.Fuselage.outer_height / 2
    z_inner = fuselage.FuselageGroup.Fuselage.inner_height / 2
    y_max = fuselage.FuselageGroup.Fuselage.outer_width / 2
    y_inner = fuselage.FuselageGroup.Fuselage.inner_width / 2
    R = max(z_max, y_max)  # not really sure since it's a cylinder, maybe just take it as a contingency
    # R_inner = max(self.FuselageGroup.Fuselage.inner_width / 2, self.FuselageGroup.Fuselage.inner_height / 2)

    # inertia thin walled oval
    area = 0.25 * np.pi * (
            fuselage.FuselageGroup.Fuselage.outer_height * fuselage.FuselageGroup.Fuselage.outer_width - fuselage.FuselageGroup.Fuselage.inner_height * fuselage.FuselageGroup.Fuselage.inner_width)
    I_zz = (np.pi * (
            fuselage.FuselageGroup.Fuselage.outer_height * fuselage.FuselageGroup.Fuselage.outer_width ** 3 - fuselage.FuselageGroup.Fuselage.inner_height * fuselage.FuselageGroup.Fuselage.inner_width ** 3)) / 64
    I_yy = (np.pi * (
            fuselage.FuselageGroup.Fuselage.outer_height ** 3 * fuselage.FuselageGroup.Fuselage.outer_width - fuselage.FuselageGroup.Fuselage.inner_height ** 3 * fuselage.FuselageGroup.Fuselage.inner_width)) / 64
    J_0 = I_zz + I_yy

    # first moment of area <-hopefully correct
    Q_outer_z = 0.25 * np.pi * z_max * y_max ** 3
    Q_outer_y = 0.25 * np.pi * z_max ** 3 * y_max
    Q_inner_z = 0.25 * np.pi * z_inner * y_inner ** 3
    Q_inner_y = 0.25 * np.pi * z_inner ** 3 * y_inner
    Q_z = Q_outer_z - Q_inner_z
    Q_y = Q_outer_y - Q_inner_y

    delta_P = np.abs(getPressure(fuselage.FuselageGroup.Aircraft.states['cruise'].altitude) - getPressure(
        fuselage.FuselageGroup.Fuselage.Cabin.cabin_pressure_altitude))

    # loading in y-/z-axis #TODO: check signs and values in these loadings
    # TODO: add loading in longitudinal direction
    # S_y = -fuselage.FuselageGroup.Tail.VerticalTail.F_w  # NEGATIVE
    # S_z = 0

    # # T = S_y * (fuselage.FuselageGroup.Tail.VerticalTail.span / 2)
    # M_y = 0
    # M_z = (fuselage.FuselageGroup.Fuselage.Cabin.length - fuselage.FuselageGroup.Aircraft.get_cg()[0]) * S_y

    # # Stress calculations
    # sigma_xA = []
    # sigma_xB = []
    # sigma_y = []
    # tau = []
    # tau_maxA = []
    # sigma_1A = []
    # sigma_2A = []
    # tau_maxB = []
    # sigma_1B = []
    # sigma_2B = []

    # for i in range(len(t)):
    #     # actual stresses
    #     sigma_xA.append(M_z * 0 / I_zz + M_y * z_max / I_yy + 2 * delta_P * R / (2 * t[i]))
    #     sigma_xB.append(M_z * y_max / I_zz + M_y * 0 / I_yy + 2 * delta_P * R / (2 * t[i]))
    #     sigma_y.append(2 * delta_P * R / t[i])
    #
    #     # sigma_x = M_z*y/I_zz + M_y*z/I_yy + 2*delta_P*R/(2*t)
    #     # sigma_y = 2*delta_P*R/t
    #
    #     tau.append(-(S_y * Q_z) / (I_zz * t[i]) - (S_z * Q_y) / (I_yy * t[i]) + T * R / J_0)
    #
    #     # design stresses
    #     tau_maxA.append(np.sqrt(((sigma_xA[i] - sigma_y[i]) / 2) ** 2 + tau[i] ** 2))
    #     sigma_1A.append((sigma_xA[i] + sigma_y[i]) / 2 + tau_maxA[i])
    #     sigma_2A.append((sigma_xA[i] + sigma_y[i]) / 2 - tau_maxA[i])
    #
    #     tau_maxB.append(np.sqrt(((sigma_xB[i] - sigma_y[i]) / 2) ** 2 + tau[i] ** 2))
    #     sigma_1B.append((sigma_xB[i] + sigma_y[i]) / 2 + tau_maxB[i])
    #     sigma_2B.append((sigma_xB[i] + sigma_y[i]) / 2 - tau_maxB[i])
    #
    # plt.figure()
    # plt.plot(t, tau_maxA)
    # plt.show()


def calculate_stress(y, z, t, aircraft):
    # Base the radius on the y and z coordinates of the point
    r = (y ** 2 + z ** 2) ** 0.5

    S_y = -aircraft.FuselageGroup.Tail.VerticalTail.F_w
    S_z = 0
    M_z = (aircraft.FuselageGroup.Fuselage.Cabin.length - aircraft.FuselageGroup.Aircraft.get_cg()[0]) * S_y
    M_y = 0
    T = S_y * (aircraft.FuselageGroup.Tail.VerticalTail.span / 2)

    # first moment of area
    a = aircraft.FuselageGroup.Fuselage.outer_height
    b = aircraft.FuselageGroup.Fuselage.outer_width

    Q_z = 4 * b ** 2 * a / 3 - (4 * (b - t) ** 2 * (a - t) / 3)
    Q_y = 4 * a ** 2 * b / 3 - (4 * (a - t) ** 2 * (b - t) / 3)

    I_yy = (np.pi * (
            aircraft.FuselageGroup.Fuselage.outer_height ** 3 * aircraft.FuselageGroup.Fuselage.outer_width - aircraft.FuselageGroup.Fuselage.inner_height ** 3 * aircraft.FuselageGroup.Fuselage.inner_width)) / 64
    I_zz = (np.pi * (
            aircraft.FuselageGroup.Fuselage.outer_height * aircraft.FuselageGroup.Fuselage.outer_width ** 3 - aircraft.FuselageGroup.Fuselage.inner_height * aircraft.FuselageGroup.Fuselage.inner_width ** 3)) / 64
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

