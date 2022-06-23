import pydoc
import typing
import functools
from uuid import uuid4
from django.conf import settings

T = typing.TypeVar("T")
MODEL_TRANSFORMERS = getattr(settings, "MODEL_TRANSFORMERS", [])
ACCESS_METHOD = getattr(
    settings,
    "KARRIO_ENTITY_ACCESS_METHOD",
    "karrio.server.core.middleware.WideAccess",
)
get_access_filter = pydoc.locate(ACCESS_METHOD)()


def uuid(prefix: str = None):
    return f'{prefix or ""}{uuid4().hex}'


class ControlledAccessModel:
    @classmethod
    def access_by(cls, context):
        if hasattr(cls, "created_by"):
            key = "created_by"
        else:
            key = "user"

        return cls.objects.filter(get_access_filter(context, key))


def register_model(model: T) -> T:
    transform = lambda model, transformer: pydoc.locate(transformer)(model)

    return functools.reduce(transform, MODEL_TRANSFORMERS, model)
