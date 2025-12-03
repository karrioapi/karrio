import re
import typing
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from karrio.server.core.logging import logger

import karrio.lib as lib
import karrio.core.errors as sdk
from karrio.server.core.datatypes import Error, Message


class ValidationError(exceptions.ValidationError, sdk.ValidationError):
    pass


# Default error levels based on HTTP status codes
# These can be overridden by setting the `level` attribute on exceptions
ERROR_LEVEL_DEFAULTS = {
    # 4xx Client Errors
    400: "error",      # Bad Request
    401: "error",      # Unauthorized
    403: "error",      # Forbidden
    404: "warning",    # Not Found - often informational
    405: "error",      # Method Not Allowed
    409: "error",      # Conflict
    422: "error",      # Unprocessable Entity
    429: "warning",    # Too Many Requests - rate limiting
    # 5xx Server Errors
    500: "error",      # Internal Server Error
    502: "error",      # Bad Gateway
    503: "warning",    # Service Unavailable - temporary
    504: "error",      # Gateway Timeout
}


def get_default_level(status_code: int, exc: typing.Optional[Exception] = None) -> str:
    """Get the default error level based on status code.

    Priority:
    1. Exception's explicit `level` attribute (if set)
    2. Status code mapping from ERROR_LEVEL_DEFAULTS
    3. Default to "error" for 4xx/5xx, "info" for others
    """
    # Check if exception has an explicit level set
    if exc is not None and hasattr(exc, "level") and exc.level is not None:
        return exc.level

    # Use status code mapping
    if status_code in ERROR_LEVEL_DEFAULTS:
        return ERROR_LEVEL_DEFAULTS[status_code]

    # Default based on status code range
    if 400 <= status_code < 500:
        return "error"
    elif status_code >= 500:
        return "error"

    return "info"


class APIException(exceptions.APIException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input.")
    default_code = "failure"
    default_level = None  # None means use status code default

    def __init__(self, detail=None, code=None, status_code=None, level=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if status_code is None:
            status_code = self.default_status_code
        if level is None:
            level = self.default_level

        self.status_code = status_code
        self.code = code
        self.detail = detail
        self.level = level


class IndexedAPIException(APIException):
    def __init__(self, index=None, **kwargs):
        super().__init__(**kwargs)
        self.index = index


class APIExceptions(APIException):
    pass


def custom_exception_handler(exc, context):
    from django.conf import settings

    # Extract request details and log exception
    request_details = _get_request_details(context)
    _log_exception(exc, request_details, debug=getattr(settings, "DEBUG", False))

    # Capture exception to telemetry (Sentry/OTEL/Datadog)
    # This ensures handled exceptions are still tracked in APM
    _capture_exception_to_telemetry(exc, request_details, context)

    response = exception_handler(exc, context)
    detail = getattr(exc, "detail", None)
    messages = message_handler(exc)
    code = get_code(exc)

    if isinstance(exc, exceptions.ValidationError) or isinstance(
        exc, sdk.ValidationError
    ):
        response_status = status.HTTP_400_BAD_REQUEST
        level = get_default_level(response_status, exc)
        formatted_errors = _format_validation_errors(detail, level=level) if detail else None
        return Response(
            messages
            or dict(
                errors=lib.to_dict(
                    formatted_errors
                    or [
                        Error(
                            code=code or "validation",
                            message=detail if isinstance(detail, str) else None,
                            level=level,
                            details=(detail if not isinstance(detail, str) else None),
                        )
                    ]
                )
            ),
            status=response_status,
            headers=getattr(response, "headers", None),
        )

    if isinstance(exc, ObjectDoesNotExist):
        response_status = status.HTTP_404_NOT_FOUND
        level = get_default_level(response_status, exc)
        resource_name = _get_resource_name(exc)
        message = f"{resource_name} not found" if resource_name else (
            detail if isinstance(detail, str) else "Resource not found"
        )
        return Response(
            dict(
                errors=lib.to_dict(
                    [
                        Error(
                            code=code or "not_found",
                            message=message,
                            level=level,
                            details=(detail if not isinstance(detail, str) else None),
                        )
                    ]
                )
            ),
            status=response_status,
            headers=getattr(response, "headers", None),
        )

    if isinstance(exc, APIExceptions):
        response_status = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        level = get_default_level(response_status, exc)
        errors = error_handler(exc, level=level)
        if errors is not None:
            return Response(
                lib.to_dict(errors),
                status=response_status,
                headers=getattr(response, "headers", None),
            )

    if isinstance(exc, APIException) or isinstance(exc, exceptions.APIException):
        response_status = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        level = get_default_level(response_status, exc)
        return Response(
            messages
            or dict(
                errors=lib.to_dict(
                    [
                        Error(
                            code=code,
                            message=detail if isinstance(detail, str) else None,
                            level=level,
                            details=(detail if not isinstance(detail, str) else None),
                        )
                    ]
                )
            ),
            status=response_status,
            headers=getattr(response, "headers", None),
        )

    elif isinstance(exc, Exception):
        response_status = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        level = get_default_level(response_status, exc)
        message, *_ = list(exc.args)
        return Response(
            dict(errors=lib.to_dict([Error(code=code, message=message, level=level)])),
            status=response_status,
            headers=getattr(response, "headers", None),
        )

    return response


def message_handler(exc) -> typing.Optional[dict]:
    if (
        hasattr(exc, "detail")
        and isinstance(exc.detail, list)
        and len(exc.detail) > 0
        and isinstance(exc.detail[0], Message)
    ):
        return dict(
            messages=lib.to_dict(
                [
                    dict(
                        code=msg.code,
                        message=msg.message,
                        level=msg.level,
                        details=msg.details,
                        carrier_id=msg.carrier_id,
                        carrier_name=msg.carrier_name,
                    )
                    for msg in typing.cast(typing.List[Message], exc.detail)
                ]
            )
        )

    return None


def error_handler(exc, level: str = "error") -> typing.Optional[dict]:
    if (
        hasattr(exc, "detail")
        and isinstance(exc.detail, list)
        and len(exc.detail) > 0
        and isinstance(exc.detail[0], Exception)
    ):
        errors: typing.List[dict] = []

        for error in exc.detail:
            message, *_ = list(exc.args)
            detail = getattr(error, "detail", None)
            index = getattr(error, "index", None)
            code = get_code(error) or "error"
            # Allow individual errors to override the level
            error_level = getattr(error, "level", None) or level
            errors.append(
                dict(
                    index=index,
                    code=code,
                    message=(
                        (detail if isinstance(detail, str) else None)
                        if detail
                        else message
                    ),
                    level=error_level,
                    details=(detail if not isinstance(detail, str) else None),
                )
            )

        return dict(errors=errors)

    return None


def get_code(exc):
    from karrio.server.core.utils import failsafe

    if hasattr(exc, "get_codes"):
        return (
            failsafe(lambda: exc.get_codes())
            or getattr(exc, "code", None)
            or getattr(exc, "default_code", None)
        )

    return getattr(exc, "default_code", None)


def _get_request_details(context: dict) -> dict:
    """Extract request details from context for logging."""
    request = context.get("view", None) and context.get("view").request

    if not request:
        return {}

    return {
        "method": getattr(request, "method", None),
        "path": getattr(request, "path", None),
        "user": str(getattr(request, "user", None)),
        "user_id": getattr(getattr(request, "user", None), "id", None),
        "query_params": dict(getattr(request, "GET", {})),
        "content_type": getattr(request, "content_type", None),
    }


def _capture_exception_to_telemetry(exc: Exception, request_details: dict, context: dict):
    """Capture exception to APM telemetry (Sentry/OTEL/Datadog).

    This ensures that handled exceptions (which return proper HTTP responses)
    are still tracked in external APM tools for visibility and alerting.
    """
    from karrio.server.core.utils import failsafe

    def _capture():
        from karrio.server.core.telemetry import get_telemetry_for_request

        telemetry = get_telemetry_for_request()
        status_code = getattr(exc, "status_code", 500)

        # Build context for the exception
        exc_context = {
            "exception_type": type(exc).__name__,
            "status_code": status_code,
            **{k: str(v) if isinstance(v, (dict, list)) else v for k, v in request_details.items()},
        }

        # Add carrier info if available in exception detail
        detail = getattr(exc, "detail", None)
        if isinstance(detail, list) and len(detail) > 0:
            first = detail[0]
            if hasattr(first, "carrier_name"):
                exc_context["carrier_name"] = first.carrier_name
            if hasattr(first, "carrier_id"):
                exc_context["carrier_id"] = first.carrier_id

        # Build tags
        tags = {
            "error_type": type(exc).__name__,
            "status_code": str(status_code),
            "error_class": "client" if status_code < 500 else "server",
        }

        # Capture to telemetry
        telemetry.capture_exception(exc, context=exc_context, tags=tags)

        # Record error metric
        telemetry.record_metric(
            "karrio.api.exception",
            1,
            tags={
                "exception_type": type(exc).__name__,
                "status_code": str(status_code),
                "path": request_details.get("path", "unknown"),
            },
            metric_type="counter",
        )

    failsafe(_capture)


def _log_exception(exc: Exception, request_details: dict, debug: bool = False):
    """Log exception with appropriate detail level based on environment."""
    exc_type = type(exc).__name__
    exc_message = str(exc)

    # Build context dict - convert dicts to strings to avoid format string issues
    context = {
        "exception_type": exc_type,
        "exception_message": exc_message,
    }

    # Add request details, flattening nested structures
    for key, value in request_details.items():
        if isinstance(value, (dict, list)):
            # Convert to string to avoid KeyError when loguru formats the message
            context[key] = str(value)
        else:
            context[key] = value

    if debug:
        # In development, log with full traceback for better debugging
        # Use positional args to avoid format string issues with curly braces in exception messages
        logger.opt(exception=exc).error(
            "Exception in request: {} - {}",
            exc_type,
            exc_message,
            **context,
        )
    else:
        # In production, log without full traceback but with context
        logger.error(
            "Exception in request: {}",
            exc_type,
            **context,
        )


def _get_resource_name(exc: ObjectDoesNotExist) -> typing.Optional[str]:
    """Extract resource name from ObjectDoesNotExist exception."""
    exc_class_name = type(exc).__name__

    # Handle Model.DoesNotExist pattern (e.g., Address.DoesNotExist -> Address)
    if exc_class_name == "DoesNotExist" and hasattr(exc, "args") and exc.args:
        match = re.search(r"(\w+) matching query", str(exc.args[0]))
        if match:
            return match.group(1)

    # Handle ObjectDoesNotExist with model info in class hierarchy
    for cls in type(exc).__mro__:
        if cls.__name__ not in ("DoesNotExist", "ObjectDoesNotExist", "Exception", "BaseException", "object"):
            return cls.__name__

    return None


def _format_validation_errors(
    detail: typing.Any,
    prefix: str = "",
    level: str = "error",
) -> typing.Optional[typing.List[Error]]:
    """Format validation errors with items[index].field pattern for list errors."""
    if detail is None:
        return None

    if isinstance(detail, str):
        return [Error(code="validation", message=detail, level=level)]

    def _build_path(base: str, key: str) -> str:
        return f"{base}.{key}" if base else key

    def _build_index_path(base: str, index: int, field: str = None) -> str:
        index_part = f"{base}[{index}]" if base else f"items[{index}]"
        return f"{index_part}.{field}" if field else index_part

    def _flatten_errors(data: typing.Any, path: str = "") -> typing.List[Error]:
        if data is None:
            return []

        if isinstance(data, str):
            message = f"{path}: {data}" if path else data
            return [Error(code="validation", message=message, level=level)]

        if isinstance(data, dict):
            return [
                err
                for key, value in data.items()
                for err in _flatten_errors(value, _build_path(path, key))
            ]

        if isinstance(data, list):
            has_indexed_items = any(isinstance(item, dict) for item in data)
            if has_indexed_items:
                return [
                    err
                    for index, item in enumerate(data)
                    if item  # skip empty dicts for list rows without errors
                    for err in (
                        [
                            nested_err
                            for field, field_errors in item.items()
                            for nested_err in _flatten_errors(
                                field_errors, _build_index_path(path, index, field)
                            )
                        ]
                        if isinstance(item, dict)
                        else _flatten_errors(item, _build_index_path(path, index))
                    )
                ]
            return [
                Error(code="validation", message=f"{path}: {item}" if path else str(item), level=level)
                for item in data
                if item
            ]

        message = f"{path}: {data}" if path else str(data)
        return [Error(code="validation", message=message, level=level)]

    errors = _flatten_errors(detail, prefix)
    return errors if errors else None
