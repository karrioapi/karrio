import attr
from typing import Any, Callable, Generic, TypeVar

XML_str = str
T = TypeVar("T")


def _identity(value: Any) -> Any:
    return value


@attr.s(auto_attribs=True)
class Serializable(Generic[T]):
    value: T
    _serializer: Callable[[T], Any] = _identity

    def serialize(self) -> Any:
        return self._serializer(self.value)


@attr.s(auto_attribs=True)
class Deserializable(Generic[T]):
    value: T
    _deserializer: Callable[[T], Any] = _identity

    def deserialize(self) -> Any:
        return self._deserializer(self.value)
