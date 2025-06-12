import typing
import logging
import traceback
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

import karrio.lib as lib
import karrio.core.errors as sdk
from karrio.server.core.datatypes import Error, Message

logger = logging.getLogger(__name__)


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
    logging.error(exc)

    response = exception_handler(exc, context)
    detail = getattr(exc, "detail", None)
    messages = message_handler(exc)
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    code = get_code(exc)

    if isinstance(exc, exceptions.ValidationError) or isinstance(
        exc, sdk.ValidationError
    ):
        return Response(
            messages
            or dict(
                errors=lib.to_dict(
                    [
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
        return Response(
            dict(
                errors=lib.to_dict(
                    [
                        Error(
                            code=code or "not_found",
                            message=detail if isinstance(detail, str) else None,
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
