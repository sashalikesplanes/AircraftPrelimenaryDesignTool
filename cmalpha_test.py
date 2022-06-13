
def C_m_alpha():
    x_cg = 50
    x_acw = 40
    x_ach = 90
    horizontal_tail_ratio = self.FuselageGroup.Tail.HorizontalTail.surface_area / self.WingGroup.Wing.wing_area
    C_L_H_alpha = np.rad2deg(self.FuselageGroup.Tail.HorizontalTail.C_L_alpha)
    print('',end="\n\n\n\n\n\n")
    C_m_alpha_fus = self.FuselageGroup.Fuselage.C_m
    d_alphah_d_alpha = self.FuselageGroup.Tail.HorizontalTail.d_alphah_d_alpha
    mean_geometric_chord_wing = self.WingGroup.Wing.mean_geometric_chord
    C_L_term = np.rad2deg(self.WingGroup.Wing.C_L_alpha) * (x_cg - x_acw) / mean_geometric_chord_wing
    C_L_H_term = 0.9 * horizontal_tail_ratio * C_L_H_alpha * d_alphah_d_alpha * (x_ach - x_cg) / mean_geometric_chord_wing
    return C_L_term + C_m_alpha_fus - C_L_H_term

def neutral_point():
    C_m_alpha = self.C_m_alpha
    C_L_alpha = np.rad2deg(self.WingGroup.Wing.C_L_alpha)
    mean_geometric_chord_wing = self.WingGroup.Wing.mean_geometric_chord
    x_cg = self.cg_loaded_half_fuel[0] / mean_geometric_chord_wing
    return  (- C_m_alpha / C_L_alpha + x_cg) * mean_geometric_chord_wing
