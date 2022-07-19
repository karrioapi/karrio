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
        test_mode = (
            context.get("test_mode")
            if isinstance(context, dict)
            else getattr(context, "test_mode", None)
        )

        if hasattr(cls, "created_by"):
            key = "created_by"
        elif hasattr(cls, "actor"):
            key = "actor"
        else:
            key = "user"

        extra = (
            dict(test_mode=context.test_mode)
            if hasattr(cls, "test_mode") and test_mode is not None
            else {}
        )

        return cls.objects.filter(get_access_filter(context, key), **extra)


def register_model(model: T) -> T:
    transform = lambda model, transformer: (
        model if transformer is None else pydoc.locate(transformer)(model)
    )

    return functools.reduce(transform, MODEL_TRANSFORMERS, model)
