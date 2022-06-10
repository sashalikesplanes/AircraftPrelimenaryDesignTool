def get_neutral_point(aircraft):

    wing = aircraft.WingGroup.Wing
    x_aerodynamic_center = aircraft.x_lemac + 0.26 * wing.mean_geometric_chord


    # Effect of downwash on H Tail

    # Pitching moment coefficient due to fuselage
    fus = aircraft.FuselageGroup.Fuselage



