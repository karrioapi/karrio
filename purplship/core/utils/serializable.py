import attr
from typing import Union, Callable, Generic, TypeVar
from purplship.core.utils.xml import Element

XML_str = str
T = TypeVar('T')
SerializationSupportedTypes = Union[dict, XML_str, list]
DeserializationSupportedTypes = Union[dict, str, Element]


def _identity(value):
    return value


@attr.s(auto_attribs=True)
class Serializable(Generic[T]):
    value: T
    _serializer: Callable[[T], SerializationSupportedTypes] = _identity

    def serialize(self) -> SerializationSupportedTypes:
        return self._serializer(self.value)


@attr.s(auto_attribs=True)
class Deserializable(Generic[T]):
    value: T
    _deserializer: Callable[[T], DeserializationSupportedTypes] = _identity

    def deserialize(self) -> DeserializationSupportedTypes:
        return self._deserializer(self.value)
