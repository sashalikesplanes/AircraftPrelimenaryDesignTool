import numpy as np
from pathlib import Path

from detailedDesign.get_drag import get_drag


decimals = 3


def make_avl_file(aircraft):
    print("M:", aircraft.states["cruise"].velocity / aircraft.states["cruise"].speed_of_sound)
    mach_number = round(aircraft.states["cruise"].velocity / aircraft.states["cruise"].speed_of_sound, 5)
    S_ref = round(aircraft.WingGroup.Wing.wing_area, decimals)
    B_ref = round(aircraft.WingGroup.Wing.span, decimals)
    C_ref = round(aircraft.WingGroup.Wing.mean_geometric_chord, decimals)
    Y_le = round(aircraft.WingGroup.Wing.span / 2, decimals)
    CD_profile = round(get_drag(aircraft)[0], decimals)
    C_root = round(aircraft.WingGroup.Wing.root_chord, decimals)
    C_tip = round(aircraft.WingGroup.Wing.tip_chord, decimals)
    X_tip = round((aircraft.WingGroup.Wing.root_chord - aircraft.WingGroup.Wing.tip_chord) / 2, decimals)

    CG_pos = np.array(aircraft.get_cg())
    print("CG:", CG_pos)
    airfoil = "NACA651412"

    # The general file stuff
    txt = f"{aircraft.name}\n"
    txt += f"#Mach\n"
    txt += f" {mach_number}\n"
    txt += f"#IYsym   IZsym   Zsym\n"
    txt += f" 0       0       0.0\n"
    txt += f"#Sref    Cref    Bref\n"
    txt += f" {S_ref}  {C_ref}  {B_ref}\n"
    txt += f"#Xref    Yref    Zref\n"
    txt += f" {round(CG_pos[0], decimals)}     {round(CG_pos[1], decimals)}     {round(CG_pos[2], decimals)}\n"
    txt += f"#CDmin\n"
    txt += f"{CD_profile}\n"
    txt += f"#====================================================================\n"

    # Wing General Stuff
    txt += f"SURFACE \n"
    txt += f"Wing \n"
    txt += f"!Nchordwise  Cspace  Nspanwise  Sspace\n"
    txt += f"12           1.0     26         -1.1\n"
    txt += f"\n"
    txt += f"COMPONENT \n"
    txt += f"1\n"
    txt += f"\n"
    txt += f"YDUPLICATE \n"
    txt += f"0.0\n"
    txt += f"\n"
    txt += f"ANGLE\n"
    txt += f"0.0\n"
    txt += f"\n"
    txt += f"SCALE\n"
    txt += f"1.0   1.0   1.0\n"
    txt += f"\n"
    txt += f"# x_lemac, 0, 0\n"
    txt += f"TRANSLATE\n"
    txt += f"{round(aircraft.x_lemac, decimals)}  0.0  0.0\n"
    txt += f"\n"

    # Wing Root
    txt += f"SECTION\n"
    txt += f"#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n"
    txt += f"0.0    0.0    0.0     {C_root}    5.0  \n"
    txt += f"AFILE\n"
    txt += f"{airfoil}.dat\n"
    txt += f"\n"

    # Wing Tip
    txt += f"SECTION\n"
    txt += f"#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace\n"
    txt += f"{X_tip}    {Y_le}    0.0     {C_tip}    5.0  \n"
    txt += f"AFILE\n"
    txt += f"{airfoil}.dat\n"
    txt += f"\n"

    with open(Path("data", "avl", f"{aircraft.name}.avl"), "w") as file:
        file.write(txt)
