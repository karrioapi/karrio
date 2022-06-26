import attr
import logging
from typing import Any, Callable, Generic, TypeVar

from karrio.core.utils.helpers import identity

logger = logging.getLogger(__name__)

XML_str = str
T = TypeVar("T")


@attr.s(auto_attribs=True)
class Serializable(Generic[T]):
    value: T
    _serializer: Callable[[T], Any] = identity
    logged: bool = False

    def serialize(self) -> Any:
        serialized_value = self._serializer(self.value)

        if self.logged:
            logger.info("serialized request::" f"{serialized_value}")

        return serialized_value


@attr.s(auto_attribs=True)
class Deserializable(Generic[T]):
    value: T
    _deserializer: Callable[[T], Any] = identity
    logged: bool = False

    def deserialize(self) -> Any:
        if self.logged:
            logger.info("deserialized response::" f"{self.value}")

        return self._deserializer(self.value)
