import logging


logger = logging.getLogger("logger")


def perform_analyses(aircraft):
    logger.debug(
            f"MTOM = {aircraft.mtom:.4E} kg, OEM = {aircraft.oem:.4E} kg, Fuel Mass = {aircraft.fuel_mass:.4E}")
    logger.debug(f"{aircraft.cruise_drag = :.4E} N")
    logger.debug(f"Wing Area: {aircraft.reference_area:.2f} m2")
