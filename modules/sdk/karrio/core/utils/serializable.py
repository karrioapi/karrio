import attr
import typing

from karrio.core.utils.helpers import identity
from karrio.core.utils.logger import logger

XML_str = str
T = typing.TypeVar("T")


@attr.s(auto_attribs=True)
class Serializable(typing.Generic[T]):
    value: typing.Any
    _serializer: typing.Callable[[typing.Any], T] = identity
    _ctx: dict = {}

    def serialize(self) -> T:
        serialized_value = self._serializer(self.value)
        logger.debug(serialized_value)
        return serialized_value

    @property
    def ctx(self) -> dict:
        return self._ctx


@attr.s(auto_attribs=True)
class Deserializable(typing.Generic[T]):
    value: typing.Any
    _deserializer: typing.Callable[[typing.Any], T] = identity
    _ctx: dict = {}

    def deserialize(self) -> T:
        logger.debug(self.value)
        return self._deserializer(self.value)

    @property
    def ctx(self) -> dict:
        return self._ctx
