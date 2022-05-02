def dragModel(params, rho):
    wingDrag = 0.5 * rho * params['velocity'] ** 2 * \
        (params['wingArea'] * params['wingC_D'])
    balloonDrag = 0.5 * rho * params['velocity'] ** 2 * \
        (params['balloonArea'] * params['balloonC_D'])
    fuselageDrag = 0.5 * rho * \
        params['velocity'] ** 2 * \
        (params['fuselageArea'] * params['fuselageC_D'])
    params['totalDrag'] = wingDrag + balloonDrag + fuselageDrag
