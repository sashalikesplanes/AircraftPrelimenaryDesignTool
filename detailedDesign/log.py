import logging


def setup_custom_logger(name, debug):
    formatter = logging.Formatter(
        fmt='%(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

def set_logger_debug_level(debug=False):
    logger = logging.getLogger('logger')
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

