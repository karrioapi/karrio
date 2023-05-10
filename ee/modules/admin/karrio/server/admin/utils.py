import typing
import logging
import functools
from rest_framework import exceptions

logger = logging.getLogger(__name__)


def staff_required(func):
    @functools.wraps(func)
    def wrapper(info, **kwargs):
        if context.request.user.is_staff is False:
            raise exceptions.PermissionDenied()

        return func(info, **kwargs)

    return wrapper
