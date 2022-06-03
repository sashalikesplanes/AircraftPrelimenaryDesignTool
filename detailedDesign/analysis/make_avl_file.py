import numpy as np

from detailedDesign.get_drag import get_drag


def make_avl_file(aircraft):
    print("M:", aircraft.states["cruise"].velocity / aircraft.states["cruise"].speed_of_sound)
    print("Sref:", aircraft.WingGroup.Wing.wing_area)
    print("Bref:", aircraft.WingGroup.Wing.span)
    print("Bref/2:", aircraft.WingGroup.Wing.span / 2)
    print("Cref:", aircraft.WingGroup.Wing.mean_geometric_chord)
    print("CDmin:", get_drag(aircraft)[0])
    print("Croot:", aircraft.WingGroup.Wing.root_chord)
    print("Ctip:", aircraft.WingGroup.Wing.tip_chord)
    print("Xtip:", (aircraft.WingGroup.Wing.root_chord - aircraft.WingGroup.Wing.tip_chord) / 2)
