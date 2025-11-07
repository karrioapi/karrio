"""
Legacy logging initialization module.

DEPRECATED: This module is deprecated in favor of the new Loguru-based logging.
Use `karrio.core.utils.logger` instead.

For backward compatibility, this module still provides the init_log function,
but it now configures Loguru instead of standard logging.
"""

import warnings
from karrio.core.utils.logger import configure_logger, intercept_standard_logging


def init_log(debug: bool = None, level: int = None):
    """
    Initialize logging configuration.

    DEPRECATED: Use `configure_logger()` from `karrio.core.utils.logger` instead.

    Args:
        debug: Enable debug mode (sets level to DEBUG)
        level: Logging level (int from logging module)
    """
    warnings.warn(
        "init_log() is deprecated. Use configure_logger() from karrio.core.utils.logger instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Map old level parameter to string for Loguru
    log_level = "DEBUG" if debug else "INFO"

    if level is not None:
        import logging
        level_map = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "INFO",
            logging.WARNING: "WARNING",
            logging.ERROR: "ERROR",
            logging.CRITICAL: "CRITICAL",
        }
        log_level = level_map.get(level, "INFO")

    # Configure Loguru with the determined level
    configure_logger(level=log_level)

    # Intercept standard logging for backward compatibility
    intercept_standard_logging()
