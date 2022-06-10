def get_neutral_point(aircraft):

    wing = aircraft.WingGroup.Wing
    x_aerodynamic_center = aircraft.x_lemac + 0.26 * wing.mean_geometric_chord


    # Effect of downwash on H Tail
    d_epsilon_d_alpha = 1.62 * wing.C_L_alpha / (np.pi * wing.aspect_ratio)

    # Pitching moment coefficient due to fuselage
    fus = aircraft.FuselageGroup.Fuselage
    C_m_fuselage = fus.outer_width ** 2 * fus.length / (wing.mean_geometric_chord * wing.surface_area)



