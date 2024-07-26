import logging
import os
from logging.handlers import RotatingFileHandler

LOG_PATH = "./app/log/"
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


class CustomFormatter(logging.Formatter):
    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    grey = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s %(name)s:%(levelname)s] %(message)s - (%(filename)s:%(lineno)d)(%(process)d:%(thread)d:%(threadName)s)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class FileFormatter(logging.Formatter):
    def format(self, record):
        format = "[%(asctime)s %(name)s:%(levelname)s] %(message)s - (%(filename)s:%(lineno)d)(%(process)d:%(thread)d:%(threadName)s)"
        formatter = logging.Formatter(format)
        return formatter.format(record)


def get_logger(name: str, level=logging.DEBUG):
    # create logger with 'spam_application'
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(CustomFormatter())

    file_ch = RotatingFileHandler(
        filename=f"{LOG_PATH}/{name}.log", maxBytes=1024 * 1024 * 50, backupCount=2
    )
    file_ch.setLevel(level)
    file_ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)
    logger.addHandler(file_ch)
    return logger
