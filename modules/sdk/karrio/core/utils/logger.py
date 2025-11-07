"""
Centralized Loguru configuration for Karrio SDK.

This module provides a unified logging interface using Loguru that can be used
throughout the Karrio SDK. It intercepts standard library logging calls and
routes them through Loguru for consistent formatting and handling.

Usage:
    from karrio.core.utils.logger import logger

    logger.info("Processing shipment request")
    logger.debug("Request payload: {payload}", payload=data)
    logger.error("Failed to connect to carrier API", exc_info=True)
"""

import os
import sys
from loguru import logger as _logger
from typing import Optional


# Remove default handler
_logger.remove()


def get_log_level() -> str:
    """Get the log level from environment variable or default to INFO."""
    return os.getenv("KARRIO_LOG_LEVEL", "INFO").upper()


def get_log_format() -> str:
    """Get the log format string."""
    return os.getenv(
        "KARRIO_LOG_FORMAT",
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>",
    )


def should_log_to_file() -> bool:
    """Check if logging to file is enabled."""
    return os.getenv("KARRIO_LOG_FILE", "").strip() != ""


def get_log_file_path() -> Optional[str]:
    """Get the log file path from environment variable."""
    log_file = os.getenv("KARRIO_LOG_FILE", "").strip()
    return log_file if log_file else None


def configure_logger(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    diagnose: Optional[bool] = None,
    backtrace: Optional[bool] = None,
    serialize: bool = False,
    enqueue: bool = False,
):
    """
    Configure the Loguru logger with custom settings.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (if None, will check KARRIO_LOG_FILE env var)
        diagnose: Whether to enable diagnostic mode with variable values
        backtrace: Whether to enable backtrace on exceptions
        serialize: Whether to serialize logs as JSON
        enqueue: Whether to use async logging (thread-safe)

    Environment Variables:
        KARRIO_LOG_LEVEL: Set the logging level (default: INFO)
        KARRIO_LOG_FORMAT: Custom log format string
        KARRIO_LOG_FILE: Path to log file for file output
        KARRIO_LOG_ROTATION: Log rotation setting (default: "500 MB")
        KARRIO_LOG_RETENTION: Log retention setting (default: "10 days")
        KARRIO_LOG_DIAGNOSE: Enable diagnostic mode (default: False)
        KARRIO_LOG_BACKTRACE: Enable backtrace (default: True)
    """
    # Remove all existing handlers
    _logger.remove()

    # Determine configuration from environment or parameters
    log_level = level or get_log_level()
    log_format = get_log_format()

    if diagnose is None:
        diagnose = os.getenv("KARRIO_LOG_DIAGNOSE", "False").lower() in (
            "true",
            "1",
            "yes",
        )

    if backtrace is None:
        backtrace = os.getenv("KARRIO_LOG_BACKTRACE", "True").lower() in (
            "true",
            "1",
            "yes",
        )

    # Add console handler
    _logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=True,
        diagnose=diagnose,
        backtrace=backtrace,
        enqueue=enqueue,
        serialize=serialize,
    )

    # Add file handler if configured
    log_file_path = log_file or get_log_file_path()
    if log_file_path:
        rotation = os.getenv("KARRIO_LOG_ROTATION", "500 MB")
        retention = os.getenv("KARRIO_LOG_RETENTION", "10 days")

        _logger.add(
            log_file_path,
            format=log_format,
            level=log_level,
            rotation=rotation,
            retention=retention,
            compression="zip",
            diagnose=diagnose,
            backtrace=backtrace,
            enqueue=enqueue,
            serialize=serialize,
        )
        _logger.info(f"File logging enabled: {log_file_path}")


def intercept_standard_logging():
    """
    Intercept standard library logging and route it through Loguru.

    This allows third-party libraries using standard logging to benefit
    from Loguru's features and consistent formatting.
    """
    import logging

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level if it exists
            level: str | int
            try:
                level = _logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where the logged message originated
            frame, depth = sys._getframe(6), 6
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            _logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Remove all existing handlers and add our interceptor
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


# Initialize logger with default configuration
configure_logger()


# Export the configured logger
logger = _logger


# Optional: Auto-intercept standard logging
# Uncomment the line below to automatically intercept all standard library logging
# intercept_standard_logging()


__all__ = ["logger", "configure_logger", "intercept_standard_logging"]
