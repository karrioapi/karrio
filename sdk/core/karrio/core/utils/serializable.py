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
    _ctx: dict = {}

    def serialize(self) -> Any:
        serialized_value = self._serializer(self.value)
        logger.debug(serialized_value)
        return serialized_value

    @property
    def ctx(self) -> dict:
        return self._ctx


@attr.s(auto_attribs=True)
class Deserializable(Generic[T]):
    value: T
    _deserializer: Callable[[T], Any] = identity
    _ctx: dict = {}

    def deserialize(self) -> Any:
        logger.debug(self.value)
        return self._deserializer(self.value)

    @property
    def ctx(self) -> dict:
        return self._ctx
