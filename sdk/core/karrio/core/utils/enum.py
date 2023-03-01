import attr
from typing import Optional, Type, Any, Callable, cast
from enum import Enum as BaseEnum, Flag as BaseFlag, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        if item is None:
            return False
        if isinstance(item, str):
            return item in cls.__members__

        return super().__contains__(item)

    def map(cls, key: Any):
        if key in cls:
            return EnumWrapper(key, cls[key])
        elif key in cast(Any, cls)._value2member_map_:
            return EnumWrapper(key, cls(key))
        elif key in [str(v.value) for v in cast(Any, cls).__members__.values()]:
            return EnumWrapper(
                key,
                next(v for v in cast(Any, cls).__members__.values() if v.value == key),
            )

        return EnumWrapper(key)

    def as_dict(self):
        return {name: enum.value for name, enum in self.__members__.items()}


class Enum(BaseEnum, metaclass=MetaEnum):
    pass


class Flag(BaseFlag, metaclass=MetaEnum):
    pass


@attr.s(auto_attribs=True)
class EnumWrapper:
    key: Any
    enum: Optional[Enum] = None

    @property
    def name(self):
        return getattr(self.enum, "name", None)

    @property
    def value(self):
        return getattr(self.enum, "value", None)

    @property
    def name_or_key(self):
        return getattr(self.enum, "name", self.key)

    @property
    def value_or_key(self):
        return getattr(self.enum, "value", self.key)

    @property
    def object(self):
        self.enum


@attr.s(auto_attribs=True)
class OptionEnum:
    code: str
    type: Callable = str
    state: Any = None

    def __getitem__(self, type: Callable = None) -> "OptionEnum":
        return OptionEnum("", type or self.type, self.state)

    def __call__(self, value: Any = None) -> "OptionEnum":
        state = self.state

        # if type is bool we have an option defined as Flag.
        if self.type is bool:
            state = value is not False

        else:
            state = self.type(value) if value is not None else None

        return OptionEnum(self.code, self.type, state)


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
    def asFlag(key: str) -> "Spec":
        """A Spec defined as "Flag" means that when it is specified in the payload,
        a boolean flag will be returned as value.
        """

        def compute(value: Optional[bool]) -> bool:
            return value is not False

        return Spec(key, bool, compute)

    @staticmethod
    def asKey(key: str) -> "Spec":
        """A Spec defined as "Key" means that when it is specified in a payload and not flagged as False,
        the spec code will be returned as value.
        """

        def compute(value: Optional[bool]) -> str:
            return key if (value is not False) else None

        return Spec(key, bool, compute)

    @staticmethod
    def asValue(key: str, type: Type = str) -> "Spec":
        """A Spec defined as "Type" means that when it is specified in a payload,
        the value passed by the user will be returned.
        """

        def compute(value: Optional[type]) -> type:  # type: ignore
            return type(value) if value is not None else None

        return Spec(key, type, compute)

    @staticmethod
    def asKeyVal(key: str, type: Type = str) -> "Spec":
        """A Spec defined as "Value" means that when it is specified in a payload,
        the a new spec defined as type is returned.
        """

        def compute_inner_spec(value: Optional[type]) -> Spec:  # type: ignore
            computed_value = (
                getattr(value, "value", None)
                if hasattr(value, "value")
                else (type(value) if value is not None else None)
            )

            return Spec(key, type, lambda *_: computed_value, computed_value)

        return Spec(key, type, compute_inner_spec)


class svcEnum(str):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, svcEnum):
            return False
        return __o == self.value