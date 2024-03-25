import enum
import typing
import logging
import functools
import strawberry
import rest_framework.exceptions as exceptions
import karrio.server.pricing.serializers as serializers

logger = logging.getLogger(__name__)

SurchargeTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("SurchargeTypeEnum", serializers.SURCHAGE_TYPE)
)


def staff_required(func):
    @functools.wraps(func)
    def wrapper(info, **kwargs):
        if info.context.request.user.is_staff is False:
            raise exceptions.PermissionDenied()

        return func(info, **kwargs)

    return wrapper


def superuser_required(func):
    @functools.wraps(func)
    def wrapper(info, **kwargs):
        if info.context.request.user.is_superuser is False:
            raise exceptions.PermissionDenied()

        return func(info, **kwargs)

    return wrapper
