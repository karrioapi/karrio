import attr
from typing import Optional, Type, Any, Callable
from enum import Enum as BaseEnum, Flag as BaseFlag, EnumMeta


class MetaEnum(EnumMeta):

    def __contains__(cls, item):
        if item is None:
            return False
        if isinstance(item, str):
            return item in cls.__members__

        return super().__contains__(item)


class Enum(BaseEnum, metaclass=MetaEnum):
    pass


class Flag(BaseFlag, metaclass=MetaEnum):
    pass


@attr.s(auto_attribs=True)
class Spec:
    key: str
    type: Type
    compute: Callable
    value: Any = None

    def apply(self, *args, **kwargs):
        return self.compute(*args, **kwargs)

    """Spec initialization modes"""

    @staticmethod
    def asFlag(key: str) -> 'Spec':
        """A Spec defined as "Flag" means that when it is specified in the payload,
            a boolean flag will be returned as value.
        """
        def compute(value: Optional[bool]) -> bool:
            return value is not False

        return Spec(key, bool, compute)

    @staticmethod
    def asKey(key: str) -> 'Spec':
        """A Spec defined as "Key" means that when it is specified in a payload and not flagged as False,
            the spec code will be returned as value.
        """
        def compute(value: Optional[bool]) -> str:
            return key if (value is not False) else None

        return Spec(key, bool, compute)

    @staticmethod
    def asValue(key: str, type: Type = str) -> 'Spec':
        """A Spec defined as "Type" means that when it is specified in a payload,
            the value passed by the user will be returned.
        """
        def compute(value: Optional[type]) -> type:  # type: ignore
            return type(value) if value is not None else None

        return Spec(key, type, compute)

    @staticmethod
    def asKeyVal(key: str, type: Type = str) -> 'Spec':
        """A Spec defined as "Value" means that when it is specified in a payload,
            the a new spec defined as type is returned.
        """
        def compute_inner_spec(value: Optional[type]) -> Spec:  # type: ignore
            computed_value = type(value) if value is not None else None

            return Spec(key, type, lambda *_: computed_value, computed_value)

        return Spec(key, type, compute_inner_spec)
