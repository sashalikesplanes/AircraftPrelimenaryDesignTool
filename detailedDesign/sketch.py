import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def sketch_aircraft(aircraft):
    plt.figure()
    plt.grid()
    things = aircraft.plot_cgs()
    for thing in things:
        plt.scatter(thing[0][0], thing[0][2])
        plt.annotate(thing[1], (thing[0][0], thing[0][2]))
        # print(thing[1], (thing[0][0], thing[0][2]))
    plt.title("CG positions relative to nose")
    plt.xlabel("Longitudanal postion [m]")
    plt.ylabel("Height position [m]")

    # plot fuselage
    length = aircraft.FuselageGroup.Fuselage.length
    diameter = aircraft.FuselageGroup.Fuselage.outer_height
    radius = diameter / 2
    tail_length = aircraft.FuselageGroup.Fuselage.tail_length

    cabin_length = aircraft.FuselageGroup.Fuselage.Cabin.length
    cabin_offset = aircraft.FuselageGroup.Fuselage.cockpit_length

    plt.plot([cabin_offset, cabin_offset], [radius, -radius], "b--")
    plt.plot([cabin_offset + cabin_length, cabin_offset + cabin_length], [radius, -radius], 'b--')

    # print(f"Slenderness ratio: {length / diameter}")
    x = [0, 0, length, length-tail_length, 0]
    y = [radius, -radius, -radius, radius, radius]
    plt.plot(x, y, "b")
    # plot mac
    offset = aircraft.WingGroup.pos
    mac = aircraft.WingGroup.Wing.mean_geometric_chord
    thiccness = aircraft.WingGroup.Wing.thickness_chord_ratio * mac / 2
    y = np.array([thiccness, -thiccness, -thiccness, thiccness, thiccness]) + offset[2]
    x = np.array([0, 0, mac, mac, 0]) + offset[0]
    plt.plot(x, y, "r")

    # vertical tail
    offset = aircraft.FuselageGroup.Tail.pos
    thiccness = aircraft.FuselageGroup.Tail.VerticalTail.span
    mac = aircraft.FuselageGroup.Tail.VerticalTail.mean_geometric_chord
    y = np.array([0, -thiccness, -thiccness, 0, 0]) + offset[2]
    x = np.array([0, 0, -mac, -mac, 0]) + offset[0]
    plt.plot(x, y, "g")

    # Horizontal tail
    offset = aircraft.FuselageGroup.Tail.pos
    mac = aircraft.FuselageGroup.Tail.HorizontalTail.mean_geometric_chord
    thiccness = aircraft.FuselageGroup.Tail.HorizontalTail.toverc * mac / 2
    y = np.array([thiccness, -thiccness, -thiccness, thiccness, thiccness]) + offset[2]
    x = np.array([0, 0, -mac, -mac, 0]) + offset[0]
    plt.plot(x, y, "r")

    plt.gca().invert_yaxis()
    location = Path('plots', 'sketch.png')
    plt.axis('equal')
    plt.savefig(location)
    plt.close()
