import logging
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError as DRFValidationError,
    APIException,
)
from django.core.exceptions import ObjectDoesNotExist

from karrio.core.utils import DP
from karrio.core.errors import ValidationError as KarrioValidationError

from karrio.server.core.datatypes import Error

logger = logging.getLogger(__name__)


class ValidationError(DRFValidationError, KarrioValidationError):
    pass


class KarrioAPIException(APIException):
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


def custom_exception_handler(exc, context):
    logger.exception(exc)

    response = exception_handler(exc, context)
    code = None
    status_code = None

    if isinstance(exc, DRFValidationError) or isinstance(exc, KarrioValidationError):
        response = Response(
            dict(
                errors=[
                    Error(
                        code="validation",
                        details=exc.detail,
                    )
                ]
            ),
            status=status.HTTP_400_BAD_REQUEST,
            headers=getattr(response, "headers", None),
        )

    if isinstance(exc, ObjectDoesNotExist):
        response = Response(
            dict(
                errors=[
                    Error(
                        code="not_found",
                        message=exc.detail if isinstance(exc.detail, str) else None,
                        details=(
                            DP.to_dict(exc.detail)
                            if not isinstance(exc.detail, str)
                            else None
                        ),
                    )
                ]
            ),
            status=status.HTTP_404_NOT_FOUND,
            headers=getattr(response, "headers", None),
        )

    if isinstance(exc, KarrioAPIException):
        response = Response(
            dict(
                errors=[
                    DP.to_dict(
                        Error(
                            code=exc.code,
                            message=exc.detail if isinstance(exc.detail, str) else None,
                            details=(
                                DP.to_dict(exc.detail)
                                if not isinstance(exc.detail, str)
                                else None
                            ),
                        )
                    )
                ]
            ),
            status=exc.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers=getattr(response, "headers", None),
        )

    elif isinstance(exc, APIException):
        response = Response(
            dict(
                errors=[
                    DP.to_dict(
                        Error(
                            code=code,
                            message=exc.detail if isinstance(exc.detail, str) else None,
                            details=(
                                DP.to_dict(exc.get_full_details())
                                if not isinstance(exc.detail, str)
                                else None
                            ),
                        )
                    )
                ]
            ),
            status=status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers=getattr(response, "headers", None),
        )

    elif isinstance(exc, Exception):
        message, *_ = list(exc.args)
        response = Response(
            dict(errors=[DP.to_dict(Error(code=code, message=message))]),
            status=status_code or status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers=getattr(response, "headers", None),
        )

    return response
