import numpy as np
import matplotlib.pyplot as plt


def sketch_aircraft(aircraft):
    print("Plotting things")
    plt.figure(2)
    things = aircraft.plot_cgs()
    print(things)
    for thing in things:
        plt.scatter(thing[0][0], thing[0][2])
        plt.annotate(thing[1], (thing[0][0], thing[0][2]))
    plt.title("CG positions relative to nose")
    plt.xlabel("Longitudanal postion [m]")
    plt.ylabel("Height position [m]")

    # plot fuselage
    length = aircraft.FuselageGroup.Fuselage.length
    diameter = aircraft.FuselageGroup.Fuselage.outer_diameter
    radius = diameter / 2
    print(f"Slenderness ratio: {length / diameter}")
    x = [0, 0, length, length, 0]
    y = [radius, -radius, -radius, radius, radius]
    plt.plot(x, y)
    # plot mac
    offset = aircraft.WingGroup.pos
    mac = aircraft.WingGroup.Wing.mean_geometric_chord
    thiccness = aircraft.WingGroup.Wing.thickness_chord_ratio * mac / 2
    y = np.array([thiccness, -thiccness, -thiccness, thiccness, thiccness]) + offset[2]
    x = np.array([0, 0, mac, mac, 0]) + offset[0]
    plt.plot(x, y)

    # vertical tail
    offset = aircraft.FuselageGroup.Tail.pos
    thiccness = aircraft.FuselageGroup.Tail.VerticalTail.span
    mac = aircraft.FuselageGroup.Tail.VerticalTail.mean_geometric_chord
    y = np.array([0, -thiccness, -thiccness, 0, 0]) + offset[2]
    x = np.array([0, 0, -mac, -mac, 0]) + offset[0]
    plt.plot(x, y)

    plt.gca().invert_yaxis()
    plt.show()
    print("Plotted things")