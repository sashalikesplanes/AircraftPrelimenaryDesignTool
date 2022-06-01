import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from pathlib import Path


def get_MTOM_from_historical_relations(aircraft, plot=False):
    designPAX = aircraft.FuselageGroup.Fuselage.Cabin.passenger_count

    # second 400 pax is iffy
    aircraftPaxMTOW = np.array(
        [(400, 177672.131), (600, 278732.511), (800, 381017.591),  # (400, 266440.158)]) Range = 10000 km
         (200, 81419.8304), (400, 152044.162), (600, 231241.39), (800, 316380.678)])  # Range = 5500 km

    PAX = [x[0] for x in aircraftPaxMTOW]
    MTOW = [x[1] for x in aircraftPaxMTOW]

    x = np.linspace(0, designPAX, 1000)

    def opt_fit(x, a, b):
        opt = a * x + b
        return opt

    # Minimises LSE
    tst = scipy.optimize.curve_fit(opt_fit, PAX, MTOW)

    # Fitted values of a and b in opt_fit
    a = tst[0][0]
    b = tst[0][1]

    j = a * x + b

    # for i in range(1000, designPAX + 500, 500):
    #     print(f" pax: {i} MTOW: {a * i + b}")

    MTOWdesPAX = a * designPAX + b

    if plot:
        print(f"pax: {designPAX} MTOW: {a * designPAX + b}")

        plt.figure()
        plt.title(f"Historical LH2 relations: MTOW vs PAX")
        plt.scatter(PAX, MTOW)
        plt.plot(x, j)
        plt.xlabel("PAX [-]")
        plt.ylabel("MTOW [kg]")
        histRelationsPath = Path("plots", "historicalRelations")
        plt.savefig(histRelationsPath, dpi=600)
        # plt.show()

    return MTOWdesPAX
