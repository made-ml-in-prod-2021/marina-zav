import logging
import sys


def init_logger(log_name) -> logging.Logger:
    """
    Initialization of logger
    """
    logger = logging.getLogger(log_name)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s {%(filename)s:%(lineno)d}{%(funcName)s}: %(message)s",
        "%y/%m/%d %H:%M:%S",
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    return logger
