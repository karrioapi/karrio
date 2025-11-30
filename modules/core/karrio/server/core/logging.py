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


def _is_sentry_enabled() -> bool:
    """Check if Sentry is configured and enabled."""
    try:
        from django.conf import settings
        return bool(getattr(settings, "SENTRY_DSN", None))
    except Exception:
        return False


def _sentry_sink(message):
    """Loguru sink that sends logs to Sentry.

    - ERROR and CRITICAL level logs are sent as Sentry events
    - WARNING level logs are added as Sentry breadcrumbs
    - INFO and DEBUG logs are ignored (too noisy for Sentry)
    """
    try:
        import sentry_sdk

        record = message.record
        level = record["level"].name
        log_message = record["message"]

        # Build extra context from record
        extra = dict(record.get("extra", {}))
        extra["logger"] = record["name"]
        extra["function"] = record["function"]
        extra["line"] = record["line"]
        extra["file"] = record["file"].name if record["file"] else None

        if level in ("ERROR", "CRITICAL"):
            # Send as Sentry event
            exception = record.get("exception")
            if exception:
                # If there's an exception, capture it
                exc_type, exc_value, exc_tb = exception.value
                if exc_value:
                    with sentry_sdk.push_scope() as scope:
                        scope.set_context("loguru", extra)
                        scope.set_tag("log_level", level)
                        sentry_sdk.capture_exception(exc_value)
            else:
                # No exception, send as message
                with sentry_sdk.push_scope() as scope:
                    scope.set_context("loguru", extra)
                    scope.set_tag("log_level", level)
                    sentry_sdk.capture_message(
                        log_message,
                        level="error" if level == "ERROR" else "fatal"
                    )

        elif level == "WARNING":
            # Add as breadcrumb for context
            sentry_sdk.add_breadcrumb(
                message=log_message,
                category="loguru",
                level="warning",
                data=extra,
            )

    except ImportError:
        # Sentry not installed
        pass
    except Exception:
        # Fail silently - don't let logging errors break the app
        pass


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

    # Add Sentry handler if Sentry is configured
    if _is_sentry_enabled():
        _logger.add(
            _sentry_sink,
            level="WARNING",  # Only WARNING and above go to Sentry
            format="{message}",  # Simple format for Sentry
            enqueue=True,  # Async to not block
            backtrace=True,
            diagnose=False,  # Don't include verbose diagnostics in Sentry
        )
        _logger.info("Sentry logging handler enabled")

    # Intercept Django's standard logging
    if intercept_django:
        intercept_standard_logging()

    # Configure third-party library loggers
    configure_third_party_loggers(debug_mode)

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


def configure_third_party_loggers(debug_mode: bool = False):
    """
    Configure logging levels for third-party libraries to reduce noise.

    In production, we suppress verbose warnings from libraries that don't provide
    useful context. In development, we keep them at WARNING level for debugging.
    """
    import logging

    # Configure jstruct logger
    # Note: jstruct logs "unknown arguments" warnings which are handled more verbosely
    # by our own code in karrio.core.utils.dict.DICTPARSE.to_object
    jstruct_logger = logging.getLogger("jstruct.utils")

    if debug_mode:
        # In debug mode, let our enhanced logging handle unknown arguments
        # Suppress jstruct's basic warnings to avoid duplicates
        jstruct_logger.setLevel(logging.ERROR)
    else:
        # In production, completely silence jstruct warnings
        # (they're typically not actionable in production)
        jstruct_logger.setLevel(logging.ERROR)

    # Configure WeasyPrint/CSS parsing loggers to suppress CSS warnings
    # WeasyPrint uses cssutils/tinycss2 which emit verbose CSS parsing warnings
    # These warnings are typically not actionable and clutter the logs
    css_loggers = [
        "weasyprint",
        "weasyprint.css",
        "weasyprint.css.validation",
        "weasyprint.html",
        "cssutils",
        "cssutils.css",
        "tinycss2",
    ]

    for logger_name in css_loggers:
        css_logger = logging.getLogger(logger_name)
        # Suppress CSS parsing warnings - they're typically not useful
        # Only show ERROR level and above
        css_logger.setLevel(logging.ERROR)
        # Disable propagation to prevent warnings from bubbling up to parent loggers
        css_logger.propagate = False


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
