import os
from karrio.core.utils.logger import logger, configure_logger

# Configure logging level for tests
log_level_map = {
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL"
}
log_level_int = int(os.environ.get("LOG_LEVEL", 30))  # WARNING default
log_level = log_level_map.get(log_level_int, "WARNING")

configure_logger(level=log_level)
