from dataclasses import make_dataclass, asdict, field
from typing import Any, Optional


class DictMixin:
    """Mixin to add dict/json conversion and pretty printing."""

    def __str__(self):
        return str(asdict(self))

    def __repr__(self):
        return str(asdict(self))


def _make_class(name: str, schema: dict[str, type]):
    """Create a dataclass with the given schema, inheriting DictMixin."""
    return make_dataclass(
        name,
        [(k, v) for k, v in schema.items()],
        bases=(DictMixin,),   # inherit our mixin
        repr=False            # disable auto repr so DictMixin takes effect
    )


def _make_union_class(name: str, items: list[dict[str, Any]]):
    """Create a dataclass with fields from the union of all dict keys."""
    schema: dict[str, type] = {}
    for item in items:
        for k, v in item.items():
            if k not in schema:
                schema[k] = type(v)

    fields = [(k, Optional[t], field(default=None)) for k, t in schema.items()]
    return make_dataclass(
        name,
        fields,
        bases=(DictMixin,),   # inherit DictMixin
        repr=False            # disable auto repr
    )


class _Typed:
    def __class_getitem__(cls, params):
        if isinstance(params, tuple):
            name, schema = params
        elif isinstance(params, dict):
            name, schema = "Anonymous", params
        else:
            raise TypeError("typed[...] must be (name, schema) or {schema}")

        return _make_class(name, schema)

    def __call__(self, value: Any = None, **kwargs: Any):
        # Case: typed(key="value") → single inferred object
        if value is None and kwargs:
            schema = {k: type(v) for k, v in kwargs.items()}
            cls = _make_class("Inferred", schema)
            return cls(**kwargs)

        # Case: typed([dicts...]) → list of objects
        if isinstance(value, list):
            if not value:
                return []
            if all(isinstance(item, dict) for item in value):
                cls = _make_union_class("InferredListItem", value)
                return [cls(**item) for item in value]
            else:
                raise TypeError("typed(list) only supports list of dicts")

        # Case: typed(dict(...)) → single object
        if isinstance(value, dict):
            schema = {k: type(v) for k, v in value.items()}
            cls = _make_class("InferredDict", schema)
            return cls(**value)

        raise TypeError("Unsupported call to typed")


# Exported instance
typed = _Typed()
