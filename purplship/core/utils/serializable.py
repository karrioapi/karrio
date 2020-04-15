import attr
import logging
from typing import Any, Callable, Generic, TypeVar

logger = logging.getLogger(__name__)

XML_str = str
T = TypeVar("T")


def _identity(value: Any) -> Any:
    return value


@attr.s(auto_attribs=True)
class Serializable(Generic[T]):
    value: T
    _serializer: Callable[[T], Any] = _identity

    def serialize(self) -> Any:
        serialized_value = self._serializer(self.value)
        logger.debug(serialized_value)
        return serialized_value


@attr.s(auto_attribs=True)
class Deserializable(Generic[T]):
    value: T
    _deserializer: Callable[[T], Any] = _identity

    def deserialize(self) -> Any:
        logger.debug(self.value)
        return self._deserializer(self.value)
