def lbs_to_kg(lbs):
    """
    this function converts lbs to kg
    :param lbs: pounds
    :return: kg
    """
    kg = lbs / 2.20462262185
    return kg


def kg_to_lbs(kg):
    """
    this function converts kg to lbs
    :param kg: kilograms
    :return: lbs
    """
    lbs = kg * 2.20462262185
    return lbs


def kts_to_ms(kts):
    """
    this function converts kts to m/s
    :param kts: knots
    :return: m/s
    """
    ms = kts * 0.514444
    return ms


def ms_to_kts(ms):
    """
    this function converts m/s to kts
    :param ms: metre/second
    :return: kts
    """
    kts = ms / 0.514444
    return kts


def K_to_C(K):
    """
    this function converts Kelvin to Celsius
    :param K: Degree Kelvin
    :return: Degree Celsius
    """
    C = K - 273.15
    return C


def C_to_K(C):
    """
    this function converts Celsius to Kelvin
    :param C: Degree Celsius
    :return: Degree Kelvin
    """
    K = C + 273.15
    return K


def m_to_inch(m):
    """
    this function converts m to inch
    :param m: metre
    :return: inch
    """
    inch = m / 0.0254
    return inch


def inch_to_m(inch):
    """
    this function converts inch to m
    :param m: metre
    :return: ft
    """
    m = inch * 0.0254
    return m


def pa_to_psi(pa):
    """
    this function converts Pa to PSI
    :param pa: Pascal
    :return: PSI
    """
    psi = pa * 0.000145038
    return psi


def bar_to_pa(bar):
    """
    this function converts bar to Pa
    :param bar: bar
    :return: Pa
    """
    pa = 100000 * bar
    return pa


def m3_to_ft3(m3):
    """
    this function converts m3 to ft3
    :param m3: m3
    :return: ft3
    """
    ft3 = 35.3147 * m3
    return ft3


def m2_to_ft2(m2):
    """
    this function converts m2 to ft2
    :param m2: m2
    :return: ft2
    """

    ft2 = 0.092903 * m2
    return ft2


def ft_to_m(ft):
    """
    this function converts ft to m
    :param ft: feet
    :return: m
    """
    m = ft * 0.3048
    return m


def m_to_ft(m):
    """
    this function converts m to ft
    :param m: metre
    :return: ft
    """
    ft = m / 0.3048
    return ft
