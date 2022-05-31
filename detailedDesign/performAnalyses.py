import logging


logger = logging.getLogger("logger")


def perform_analyses(aircraft):
    print_summary(aircraft)


def print_summary(aircraft):
    logger.debug(
            f"MTOM = {aircraft.mtom:.4E} kg, OEM = {aircraft.oem:.4E} kg, Fuel Mass = {aircraft.fuel_mass:.4E}")
    logger.debug(f"{aircraft.cruise_drag = :.4E} N")
    logger.debug(f"Wing Area: {aircraft.reference_area:.2f} m2")
    
    engines = aircraft.WingGroup.Engines
    logger.debug(f"Amount of propellors: {engines.own_amount_prop} [-]")
    logger.debug(f"Amoung of motors: {engines.own_amount_motor} [-]")
    logger.debug(f"Unit dimensions (L x W x H) ({engines.own_lenght_unit:.3f} x {engines.own_width_unit:.3f} x {engines.own_height_unit:.3f}) [m]")
