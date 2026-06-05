import logging
import sys
import os

LOG_FILE = "battleship.log"


def reset_log_file():
    if LOG_FILE in os.listdir():
        os.remove(LOG_FILE)


def get_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        comnsole_formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
        console_handler.setFormatter(comnsole_formatter)

        file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
