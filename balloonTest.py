import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def main(compRatio):
    totalHydrogenMass = 4e3  # kg
    # compRatio = 2

    rhoHydrogenGas = 0.08375  # kg/m^3
    finesseRatio = 6  # -
    pHydrogenSeaLevel = 101325  # Pa
    T = 288.15 - 15 - 23.96

    rhoAir = 0.6601  # kg/m^3
    pAir = 4.722e4  # Pa
    hydrogenMolarMass = 2.016e-3  # kg

    R = 8.3145
    factorOfSafety = 2
    contingency = 2

    sigma_mat = 241e6  # Pa
    sigma_mat = 1900e6 / factorOfSafety  # carbon fiber
    # sigma_mat = 460e6 # steel
    factorOfSafety = 2  # -

    rho_mat = 2710  # [kg/m^3]
    rho_mat = 1550  # carbon fiber
    # rho_mat = 7850  # steel
    g = 9.79

    volume = totalHydrogenMass / \
        (rhoHydrogenGas * compRatio)

    lift = volume * g * (rhoAir)

    radius = (volume / (4 / 3 * np.pi *
              finesseRatio)) ** (1/3)

    # radius = np.pi * radius ** 2

    # Calculate mass of the balloon using plain pressure vessel
    p = totalHydrogenMass / hydrogenMolarMass * R * T / volume
    print(volume)

    dp = p - pAir

    ratio = dp / (2 * sigma_mat + dp)
    wallThickness = ratio * (2 * radius)
    # wallThickness = p * radius * \
    #     factorOfSafety / (2 * sigma_mat)
    eccentricity = (1 - (1 / finesseRatio) ** 2)
    balloonSurfaceArea = 2 * np.pi * radius ** 2 * \
        (1 + finesseRatio /
         eccentricity * np.arcsin(eccentricity))
    structuralMass = balloonSurfaceArea * \
        wallThickness * rho_mat * contingency

    return {"wallThickness": wallThickness, "volume": volume, "pressure": p, "lift": lift, "structuralMass": structuralMass, "volumetricDensity": rhoHydrogenGas * compRatio, "thicknessRadiusRatio": wallThickness / (2 * radius), "ratio": totalHydrogenMass / (totalHydrogenMass + structuralMass)}


if __name__ == "__main__":
    #  1780 tons
    # df = pd.DataFrame()
    # linspace = np.linspace(2, 700, 20)
    # for compRatio in linspace:
    #     dict = main(compRatio)
    #     df = df.append(dict, ignore_index=True)
    # print(df.head())
    # plt.plot(linspace,
    #          df["structuralMass"] * 1000)
    # plt.show()
    print(main(700))
    # plt.plot(df["pressure"] / 1e6, df["thicknessRadiusRatio"])
    # plt.show()
