import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

acRange = 10186
# second 400 pax is iffy
aircraftPaxMTOW = np.array([(400, 177672.131), (600, 278732.511), (800, 381017.591)])  # , (400, 266440.158), ])

pax = [x[0] for x in aircraftPaxMTOW]
MTOW = [x[1] for x in aircraftPaxMTOW]

x = np.linspace(0, 2500, 1000)
order = 1
s = InterpolatedUnivariateSpline(pax, MTOW, k=order)
y = s(x)

print(f"pax: 1000 MTOW: {s(1000)}, \n pax: 1500  MTOW: {s(1500)}, \n pax: 2000 MTOW: {s(2000)}")

plt.figure()
plt.title(f"Historical LH2 relations: MTOW vs PAX, range = {acRange}")
plt.scatter(pax, MTOW)
plt.plot(x, y)
plt.xlabel("PAX [-]")
plt.ylabel("MTOW [kg]")
# plt.show()
