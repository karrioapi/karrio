import attr
import enum
import typing

BaseStrEnum = getattr(enum, "StrEnum", enum.Flag)


class MetaEnum(enum.EnumMeta):
    def __contains__(cls, item):
        if item is None:
            return False
        if isinstance(item, str):
            return item in cls.__members__

        return super().__contains__(item)

    def map(cls, key: typing.Any):
        if key in cls:
            return EnumWrapper(key, cls[key])
        elif key in typing.cast(typing.Any, cls)._value2member_map_:
            return EnumWrapper(key, cls(key))
        elif key in [
            str(v.value) for v in typing.cast(typing.Any, cls).__members__.values()
        ]:
            return EnumWrapper(
                key,
                next(
                    v
                    for v in typing.cast(typing.Any, cls).__members__.values()
                    if v.value == key
                ),
            )

        return EnumWrapper(key)

    def find(cls, key: typing.Any):
        """Find an enum member where the key is contained in the member's value.

        This is useful for enums with list values (e.g., TrackingStatus, TrackingIncidentReason)
        where you need to check if a code is IN any of the list values.

        Example:
            class TrackingStatus(lib.Enum):
                delivered = ["DEL", "DL", "DELIVERED"]
                in_transit = ["IT", "OT", "IN_TRANSIT"]

            status = TrackingStatus.find("DEL").name  # "delivered"
            status = TrackingStatus.find("UNKNOWN").name  # None

        :param key: The key to search for within enum values.
        :return: EnumWrapper with the matching enum or None.
        """
        return EnumWrapper(
            key,
            next(
                (
                    member
                    for member in typing.cast(typing.Any, cls).__members__.values()
                    if (
                        key in member.value
                        if isinstance(member.value, (list, tuple))
                        else key == member.value
                    )
                ),
                None,
            ) if key is not None else None,
        )

    def as_dict(self):
        return {name: enum.value for name, enum in self.__members__.items()}


class Enum(enum.Enum, metaclass=MetaEnum):
    pass


class Flag(enum.Flag, metaclass=MetaEnum):
    pass


class StrEnum(BaseStrEnum, metaclass=MetaEnum):  # type: ignore
    pass


@attr.s(auto_attribs=True)
class EnumWrapper:
    key: typing.Any
    enum: typing.Optional[Enum] = None

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
    """An option enumeration class for handling typed options.

    Attributes:
        code: The option code or identifier
        type: The type converter function or enum type
        state: The current state value
        default: The default value to use when none is provided
        help: Help text describing the option
        meta: Optional metadata dict (e.g., dict(category="COD"))
    """
    code: str
    type: typing.Union[typing.Callable, MetaEnum] = str
    state: typing.Any = None
    default: typing.Any = None
    help: typing.Optional[str] = None
    meta: typing.Optional[dict] = None

    def __getitem__(self, type: typing.Callable = None) -> "OptionEnum":
        return OptionEnum("", type or self.type, self.state, self.default, self.help, self.meta)

    def __call__(self, value: typing.Any = None) -> "OptionEnum":
        """Create a new OptionEnum instance with the specified value.

        Args:
            value: The value to set. If None and default is provided, default will be used.

        Returns:
            A new OptionEnum instance with the appropriate state.
        """
        state = self.state

        # if value is None and default is provided, use default
        if value is None and self.default is not None:
            value = self.default

        # if type is bool we have an option defined as Flag.
        if self.type is bool:
            state = value is not False

        elif "enum" in str(self.type):
            state = (
                (
                    self.type.map(value).name_or_key  # type: ignore
                    if hasattr(value, "map")
                    else self.type[value].name  # type: ignore
                )
                if value is not None and value != ""
                else None
            )

        # Handle typing generics (e.g., typing.List[X], typing.Dict[X, Y])
        elif hasattr(self.type, "__origin__"):
            # For List types, just use the value as-is (it's already a list from JSON)
            state = value if value is not None else None

        else:
            state = self.type(value) if value is not None else None

        return OptionEnum(self.code, self.type, state, self.default, self.help, self.meta)


@attr.s(auto_attribs=True)
class Spec:
    """A specification class for handling typed values with computation logic.

    Attributes:
        key: The specification key or identifier
        type: The type of the specification value
        compute: The computation function to apply
        value: The current value
        default: The default value to use when none is provided
    """
    key: str
    type: typing.Type
    compute: typing.Callable
    value: typing.Any = None
    default: typing.Any = None

    def apply(self, *args, **kwargs):
        """Apply the computation function to the arguments."""
        return self.compute(*args, **kwargs)

    """Spec initialization modes"""

    @staticmethod
    def asFlag(key: str, default: typing.Optional[bool] = None) -> "Spec":
        """A Spec defined as "Flag" means that when it is specified in the payload,
        a boolean flag will be returned as value.

        Args:
            key: The specification key
            default: Default value to use when none is provided

        Returns:
            A Spec instance configured as a flag
        """

        def compute(value: typing.Optional[bool]) -> bool:
            # Use default if value is None
            if value is None and default is not None:
                value = default
            return value is not False

        return Spec(key, bool, compute, default=default)

    @staticmethod
    def asKey(key: str, default: typing.Optional[bool] = None) -> "Spec":
        """A Spec defined as "Key" means that when it is specified in a payload and not flagged as False,
        the spec code will be returned as value.

        Args:
            key: The specification key
            default: Default value to use when none is provided

        Returns:
            A Spec instance configured to return its key
        """

        def compute(value: typing.Optional[bool]) -> str:
            # Use default if value is None
            if value is None and default is not None:
                value = default
            return key if (value is not False) else None

        return Spec(key, bool, compute, default=default)

    @staticmethod
    def asValue(key: str, type: typing.Type = str, default: typing.Any = None) -> "Spec":
        """A Spec defined as "typing.Type" means that when it is specified in a payload,
        the value passed by the user will be returned.

        Args:
            key: The specification key
            type: The type to convert the value to
            default: Default value to use when none is provided

        Returns:
            A Spec instance configured to return the typed value
        """

        def compute(value: typing.Optional[type]) -> type:  # type: ignore
            # Use default if value is None
            if value is None and default is not None:
                value = default
            return type(value) if value is not None else None

        return Spec(key, type, compute, default=default)

    @staticmethod
    def asKeyVal(key: str, type: typing.Type = str, default: typing.Any = None) -> "Spec":
        """A Spec defined as "Value" means that when it is specified in a payload,
        the a new spec defined as type is returned.

        Args:
            key: The specification key
            type: The type to convert the value to
            default: Default value to use when none is provided

        Returns:
            A Spec instance configured to return a new Spec with the typed value
        """

        def compute_inner_spec(value: typing.Optional[type]) -> Spec:  # type: ignore
            # Use default if value is None
            if value is None and default is not None:
                value = default

            computed_value = (
                getattr(value, "value", None)
                if hasattr(value, "value")
                else (type(value) if value is not None else None)
            )

            return Spec(key, type, lambda *_: computed_value, computed_value, default=default)

        return Spec(key, type, compute_inner_spec, default=default)


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
