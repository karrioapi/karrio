import enum
import typing
import functools
import strawberry
import rest_framework.exceptions as exceptions
from strawberry.types import Info
import karrio.server.pricing.serializers as serializers
from karrio.server.core.logging import logger

# Markup type enum for GraphQL
MarkupTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    enum.Enum("MarkupTypeEnum", serializers.MARKUP_TYPE)
)


def staff_required(func):
    @functools.wraps(func)
    def wrapper(info: Info, **kwargs):
        if info.context.request.user.is_staff is False:
            raise exceptions.PermissionDenied()

        return func(info, **kwargs)

    return wrapper


def superuser_required(func):
    @functools.wraps(func)
    def wrapper(info: Info, **kwargs):
        if info.context.request.user.is_superuser is False:
            raise exceptions.PermissionDenied()

        return func(info, **kwargs)

    return wrapper
