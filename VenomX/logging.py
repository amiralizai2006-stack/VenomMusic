# All rights reserved.

import logging
import os
from logging.handlers import RotatingFileHandler


LOG_FILE = "/tmp/VenomXlogs.txt"


def setup_logging():
    handlers = [
        logging.StreamHandler(),
    ]

    # /tmp is writable on Deplexo
    try:
        os.makedirs("/tmp/VenomX", exist_ok=True)

        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5000000,
            backupCount=10,
            encoding="utf-8",
        )

        handlers.insert(0, file_handler)

    except Exception:
        # If file logging fails, continue with console logging.
        pass

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        handlers=handlers,
        force=True,
    )

    logging.getLogger("pyrogram").setLevel(logging.ERROR)
    logging.getLogger("pytgcalls").setLevel(logging.ERROR)
    logging.getLogger("pymongo").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)

    # Setting ntgcalls logger level and disabling propagation
    ntgcalls_logger = logging.getLogger("ntgcalls")
    ntgcalls_logger.setLevel(logging.CRITICAL)
    ntgcalls_logger.propagate = False


setup_logging()


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
