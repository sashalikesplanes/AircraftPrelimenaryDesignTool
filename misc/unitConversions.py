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
