import functools
import typing
from karrio.server.core.models.base import (
    ControlledAccessModel,
    get_access_filter,
    register_model,
    uuid,
)
from karrio.server.core.models.third_party import (
    APILog,
    APILogIndex,
)
from karrio.server.core.models.entity import Entity, OwnedEntity


def _identity(value: typing.Any):
    return value


def field_default(value: typing.Any) -> typing.Callable:
    return functools.partial(_identity, value=value)
