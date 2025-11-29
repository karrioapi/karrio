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


class APIException(exceptions.APIException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input.")
    default_code = "failure"

    def __init__(self, detail=None, code=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if status_code is None:
            status_code = self.default_status_code

        self.status_code = status_code
        self.code = code
        self.detail = detail


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

    response = exception_handler(exc, context)
    detail = getattr(exc, "detail", None)
    messages = message_handler(exc)
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    code = get_code(exc)

    if isinstance(exc, exceptions.ValidationError) or isinstance(
        exc, sdk.ValidationError
    ):
        formatted_errors = _format_validation_errors(detail) if detail else None
        return Response(
            messages
            or dict(
                errors=lib.to_dict(
                    formatted_errors
                    or [
                        Error(
                            code=code or "validation",
                            message=detail if isinstance(detail, str) else None,
                            details=(detail if not isinstance(detail, str) else None),
                        )
                    ]
                )
            ),
            status=status.HTTP_400_BAD_REQUEST,
            headers=getattr(response, "headers", None),
        )

    if isinstance(exc, ObjectDoesNotExist):
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
                            details=(detail if not isinstance(detail, str) else None),
                        )
                    ]
                )
            ),
            status=status.HTTP_404_NOT_FOUND,
            headers=getattr(response, "headers", None),
        )

    if isinstance(exc, APIExceptions):
        errors = error_handler(exc)
        if errors is not None:
            return Response(
                lib.to_dict(errors),
                status=status_code,
                headers=getattr(response, "headers", None),
            )

    if isinstance(exc, APIException) or isinstance(exc, exceptions.APIException):
        return Response(
            messages
            or dict(
                errors=lib.to_dict(
                    [
                        Error(
                            code=code,
                            message=detail if isinstance(detail, str) else None,
                            details=(detail if not isinstance(detail, str) else None),
                        )
                    ]
                )
            ),
            status=status_code,
            headers=getattr(response, "headers", None),
        )

    elif isinstance(exc, Exception):
        message, *_ = list(exc.args)
        return Response(
            dict(errors=lib.to_dict([Error(code=code, message=message)])),
            status=status_code,
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
                        details=msg.details,
                        carrier_id=msg.carrier_id,
                        carrier_name=msg.carrier_name,
                    )
                    for msg in typing.cast(typing.List[Message], exc.detail)
                ]
            )
        )

    return None


def error_handler(exc) -> typing.Optional[dict]:
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
            errors.append(
                dict(
                    index=index,
                    code=code,
                    message=(
                        (detail if isinstance(detail, str) else None)
                        if detail
                        else message
                    ),
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
) -> typing.Optional[typing.List[Error]]:
    """Format validation errors with items[index].field pattern for list errors."""
    if detail is None:
        return None

    if isinstance(detail, str):
        return [Error(code="validation", message=detail)]

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
            return [Error(code="validation", message=message)]

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
                Error(code="validation", message=f"{path}: {item}" if path else str(item))
                for item in data
                if item
            ]

        message = f"{path}: {data}" if path else str(data)
        return [Error(code="validation", message=message)]

    errors = _flatten_errors(detail, prefix)
    return errors if errors else None
