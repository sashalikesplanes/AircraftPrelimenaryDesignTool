import logging


logger = logging.getLogger("logger")


def perform_analyses(aircraft):
    # print(aircraft)
    logger.debug(f"{ aircraft.mtom = }")
    logger.debug(
        f"MTOM = {aircraft.mtom} kg, OEM = {aircraft.oem} kg, Fuel Mass = {aircraft.fuel_mass}")
