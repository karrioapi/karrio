import pydoc
import typing
import functools
from uuid import uuid4
from django.db import models
from django.conf import settings

import karrio.lib as lib

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
    def access_by(cls: models.Model, context, manager: str = "objects"):
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

        query = get_access_filter(context, key)

        if hasattr(cls, "test_mode") and test_mode is not None:
            query = query & models.Q(
                models.Q(test_mode=test_mode) | models.Q(test_mode__isnull=True)
            )

        queryset = getattr(cls, manager, cls.objects)

        if hasattr(cls, "resolve_context_data"):
            queryset = cls.resolve_context_data(queryset, context)

        return queryset.filter(query)

    @classmethod
    def resolve_context_data(cls, queryset, context):
        # 1. Self-optimization (e.g., Carrier resolving its own configs)
        if hasattr(queryset, 'resolve_config_for'):
            queryset = queryset.resolve_config_for(context)

        # 2. Relation optimization
        relations = getattr(cls, "CONTEXT_RELATIONS", [])
        if relations:
            from django.db.models import Prefetch
            prefetches = []

            for field_name in relations:
                field = cls._meta.get_field(field_name)
                related_model = field.related_model

                # Check if related model is capable of context resolution
                if hasattr(related_model.objects, 'resolve_config_for'):
                    qs = related_model.objects.resolve_config_for(context)
                    prefetches.append(Prefetch(field_name, queryset=qs))
                elif hasattr(related_model, 'access_by'):
                    # Recurse into related model's access_by (which calls its resolve_context_data)
                    qs = related_model.access_by(context)
                    prefetches.append(Prefetch(field_name, queryset=qs))

            if prefetches:
                queryset = queryset.prefetch_related(*prefetches)

        return queryset


def register_model(model: T) -> T:
    transform = lambda model, transformer: (
        model if transformer is None else pydoc.locate(transformer)(model)
    )

    return functools.reduce(transform, MODEL_TRANSFORMERS, model)


class MetafieldType(lib.StrEnum):
    text = "text"
    number = "number"
    boolean = "boolean"
    json = "json"
    date = "date"
    date_time = "date_time"
    password = "password"


METAFIELD_TYPE = [(c.name, c.name) for c in list(MetafieldType)]
