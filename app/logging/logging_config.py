import logging
import sys

from app.config.main import get_settings

settings = get_settings()


def setup_logging():
    """
    Set up application-wide logging configuration.
    """
    # Get the root logger
    logger = logging.getLogger()

    # Create formatter with the desired format
    formatter = logging.Formatter("[%(name)s - %(filename)s:%(lineno)d:%(funcName)s] %(levelname)s - %(message)s")

    # Create StreamHandler for console output and set the formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Avoid duplicate handlers if setup_logging is called multiple times
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        logger.addHandler(handler)

    # Set the logging level from config
    logger.setLevel(getattr(logging, settings.LOGLEVEL.upper(), logging.INFO))
