import ast
import yaml
import typing
import functools

import karrio.lib as lib
from karrio.server.core.models.base import (
    ControlledAccessModel,
    get_access_filter,
    register_model,
    uuid,
    MetafieldType,
    METAFIELD_TYPE,
)
from karrio.server.core.models.third_party import (
    APILog,
    APILogIndex,
)
from karrio.server.core.models.metafield import (
    Metafield,
)
from karrio.server.core.models.entity import Entity, OwnedEntity


def _identity(value: typing.Any):
    return value


def field_default(value: typing.Any) -> typing.Callable:
    return functools.partial(_identity, value=value)


def metafields_to_dict(metafields: typing.List[Metafield]) -> dict:
    _values = {}

    for _ in metafields:
        # Skip metafields with None or empty values
        if _.value is None or _.value == "":
            continue

        if _.type == "number":
            _values.update({_.key: lib.failsafe(lambda: ast.literal_eval(_.value))})
        elif _.type == "boolean":
            _values.update({_.key: lib.failsafe(lambda: bool(yaml.safe_load(_.value)))})
        else:
            _values.update({_.key: _.value})

    return _values
