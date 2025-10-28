"""
Django-integrated Loguru logging configuration for Karrio Server.

This module provides seamless integration between Django's logging system
and Loguru, allowing you to use Loguru's powerful features while maintaining
compatibility with Django's ecosystem.

Usage in Django settings:
    # In settings/base.py, after LOGGING configuration
    from karrio.server.core.logging import setup_django_loguru
    setup_django_loguru()

Usage in code:
    from karrio.server.core.logging import logger

    logger.info("User logged in", user_id=user.id)
    logger.error("Payment failed", error=str(e), order_id=order.id)
"""

import os
import sys
from pathlib import Path
from loguru import logger as _logger
from typing import Optional


# Remove default handler
_logger.remove()


class DjangoLoguruHandler:
    """
    Custom handler that integrates Loguru with Django's logging system.
    Preserves Django's context and request information.
    """

    def __init__(self):
        self.logger = _logger

    def write(self, message):
        """Write method for Django compatibility."""
        self.logger.opt(depth=6, colors=True).info(message)


def get_django_log_config():
    """
    Get Django-specific log configuration from Django settings.
    Falls back to environment variables if Django settings are not available.
    """
    try:
        from django.conf import settings

        return {
            "level": getattr(settings, "LOG_LEVEL", "INFO"),
            "log_file": getattr(settings, "LOG_FILE_NAME", None),
            "log_dir": getattr(settings, "LOG_FILE_DIR", None),
            "debug": getattr(settings, "DEBUG", False),
        }
    except Exception:
        # Fallback to environment variables
        return {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "log_file": os.getenv("LOG_FILE_NAME"),
            "log_dir": os.getenv("LOG_DIR"),
            "debug": os.getenv("DEBUG_MODE", "False").lower() in ("true", "1", "yes"),
        }


def get_log_format(debug: bool = False) -> str:
    """Get the log format string appropriate for Django."""
    if debug:
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level> | "
            "{extra}"
        )
    else:
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan> | "
            "<level>{message}</level>"
        )


def setup_django_loguru(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    intercept_django: bool = True,
    serialize: bool = False,
    enqueue: bool = True,
):
    """
    Set up Loguru for Django with optimal configuration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (overrides Django settings)
        intercept_django: Whether to intercept Django's logging (recommended)
        serialize: Whether to serialize logs as JSON
        enqueue: Whether to use async logging (recommended for Django)

    This function should be called in Django settings after LOGGING configuration.
    """
    # Remove all existing handlers
    _logger.remove()

    # Get configuration from Django settings or environment
    config = get_django_log_config()
    log_level = level or config["level"]
    debug_mode = config["debug"]
    log_format = get_log_format(debug_mode)

    # Add console handler with colors
    _logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=True,
        diagnose=debug_mode,
        backtrace=True,
        enqueue=enqueue,
        serialize=serialize,
    )

    # Add file handler if configured
    log_file_path = log_file or config.get("log_file")
    if log_file_path:
        # Ensure directory exists
        log_dir = Path(log_file_path).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        _logger.add(
            log_file_path,
            format=log_format,
            level=log_level,
            rotation="500 MB",
            retention="10 days",
            compression="zip",
            diagnose=debug_mode,
            backtrace=True,
            enqueue=enqueue,
            serialize=serialize,
        )
        _logger.info(f"Django file logging enabled: {log_file_path}")

    # Intercept Django's standard logging
    if intercept_django:
        intercept_standard_logging()

    _logger.info(f"Loguru configured for Django (level: {log_level})")


def intercept_standard_logging():
    """
    Intercept all standard library logging and route it through Loguru.

    This ensures that Django and all third-party libraries using standard
    logging benefit from Loguru's features and consistent formatting.
    """
    import logging

    class InterceptHandler(logging.Handler):
        """
        Handler that intercepts standard logging and forwards to Loguru.
        """

        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level
            try:
                level = _logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where the logged message originated
            frame, depth = sys._getframe(6), 6
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            # Add extra context from Django if available
            extra = {}
            if hasattr(record, "request"):
                extra["request_id"] = getattr(record.request, "id", None)
                extra["user"] = getattr(record.request, "user", None)

            _logger.opt(depth=depth, exception=record.exc_info).bind(**extra).log(
                level, record.getMessage()
            )

    # Configure root logger to use our interceptor
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(0)

    # Update all existing loggers
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    _logger.info("Standard logging interception enabled")


def get_request_context_logger(request):
    """
    Get a logger bound with request context for structured logging.

    Usage in Django views:
        from karrio.server.core.logging import get_request_context_logger

        def my_view(request):
            logger = get_request_context_logger(request)
            logger.info("Processing request")
    """
    return _logger.bind(
        request_id=getattr(request, "id", None),
        user_id=getattr(request.user, "id", None) if hasattr(request, "user") else None,
        path=request.path if hasattr(request, "path") else None,
        method=request.method if hasattr(request, "method") else None,
    )


# Create middleware for automatic request logging
class LoguruRequestLoggingMiddleware:
    """
    Django middleware that adds request/response logging with Loguru.

    Add to MIDDLEWARE in Django settings:
        'karrio.server.core.logging.LoguruRequestLoggingMiddleware',
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Bind request context
        request_logger = get_request_context_logger(request)

        # Log request
        request_logger.info(
            f"Request started: {request.method} {request.path}",
        )

        # Process request
        response = self.get_response(request)

        # Log response
        request_logger.info(
            f"Request finished: {request.method} {request.path} - Status: {response.status_code}",
            status_code=response.status_code,
        )

        return response

    def process_exception(self, request, exception):
        """Log exceptions with full context."""
        request_logger = get_request_context_logger(request)
        request_logger.exception(
            f"Request exception: {request.method} {request.path}",
            exception_type=type(exception).__name__,
        )


# Export the configured logger
logger = _logger


__all__ = [
    "logger",
    "setup_django_loguru",
    "intercept_standard_logging",
    "get_request_context_logger",
    "LoguruRequestLoggingMiddleware",
]
