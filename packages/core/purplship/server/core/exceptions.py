import logging
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError as DRFValidationError, APIException,
)
from django.core.exceptions import ObjectDoesNotExist

from purplship.core.utils import DP
from purplship.core.errors import ValidationError as PurplShipValidationError

from purplship.server.core.datatypes import Error

logger = logging.getLogger(__name__)


class ValidationError(DRFValidationError, PurplShipValidationError):
    pass


class PurplShipApiException(APIException):
    default_status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'failure'

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

    if isinstance(exc, DRFValidationError) or isinstance(exc, PurplShipValidationError):
        response.status_code = status.HTTP_400_BAD_REQUEST
        code = 'validation'

    if isinstance(exc, ObjectDoesNotExist):
        status_code = status.HTTP_404_NOT_FOUND
        code = 'not_found'

    if isinstance(exc, PurplShipApiException):
        response.status_code = exc.status_code
        response.data = dict(
            error=DP.to_dict(Error(
                code=exc.code,
                message=exc.detail if isinstance(exc.detail, str) else None,
                details=DP.to_dict(exc.detail) if not isinstance(exc.detail, str) else None
            ))
        )

    elif isinstance(exc, APIException):
        response.data = dict(
            error=DP.to_dict(Error(
                code=code,
                message=exc.detail if isinstance(exc.detail, str) else None,
                details=DP.to_dict(exc.get_full_details()) if not isinstance(exc.detail, str) else None
            ))
        )

    elif isinstance(exc, Exception):
        message, *_ = list(exc.args)
        response = Response(
            dict(error=DP.to_dict(Error(code=code, message=message))),
            status=status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
