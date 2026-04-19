import ast
import functools
import typing

import karrio.lib as lib
import yaml
from karrio.server.core.models.base import (
    METAFIELD_TYPE,
    ControlledAccessModel,
    MetafieldType,
    get_access_filter,
    register_model,
    uuid,
)
from karrio.server.core.models.entity import Entity, OwnedEntity
from karrio.server.core.models.metafield import (
    Metafield,
)
from karrio.server.core.models.third_party import (
    APILog,
    APILogIndex,
)

__all__ = [
    "METAFIELD_TYPE",
    "ControlledAccessModel",
    "MetafieldType",
    "get_access_filter",
    "register_model",
    "uuid",
    "Entity",
    "OwnedEntity",
    "Metafield",
    "APILog",
    "APILogIndex",
    "field_default",
    "metafields_to_dict",
]


def _identity(value: typing.Any):
    return value


def field_default(value: typing.Any) -> typing.Callable:
    return functools.partial(_identity, value=value)


def metafields_to_dict(metafields: list[Metafield]) -> dict:
    _values = {}

    for _ in metafields:
        # Skip metafields with None or empty values
        if _.value is None or _.value == "":
            continue

        if _.type == "number":
            _values.update({_.key: lib.failsafe(lambda _=_: ast.literal_eval(_.value))})
        elif _.type == "boolean":
            _values.update({_.key: lib.failsafe(lambda _=_: bool(yaml.safe_load(_.value)))})
        else:
            _values.update({_.key: _.value})

    return _values
