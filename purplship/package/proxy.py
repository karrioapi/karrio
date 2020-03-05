"""PurplShip Proxy base class definition module."""

import attr
from typing import TypeVar
from purplship.core.settings import Settings
from purplship.core.errors import MethodNotSupportedError
from purplship.core.utils.serializable import Deserializable, Serializable

T = TypeVar('T')
S = TypeVar('S')


@attr.s(auto_attribs=True)
class Proxy:
    """Unitied Shipping API Proxy (Interface)
    """

    settings: Settings

    def get_rates(self, request: Serializable[T]) -> Deserializable[S]:
        raise MethodNotSupportedError(self.__class__.get_rates.__name__, self.__class__.__name__)

    def get_tracking(self, request: Serializable[T]) -> Deserializable[S]:
        raise MethodNotSupportedError(self.__class__.get_tracking.__name__, self.__class__.__name__)

    def create_shipment(self, request: Serializable[T]) -> Deserializable[S]:
        raise MethodNotSupportedError(self.__class__.create_shipment.__name__, self.__class__.__name__)

    def request_pickup(self, request: Serializable[T]) -> Deserializable[S]:
        raise MethodNotSupportedError(self.__class__.request_pickup.__name__, self.__class__.__name__)

    def update_pickup(self, request: Serializable[T]) -> Deserializable[S]:
        raise MethodNotSupportedError(self.__class__.update_pickup.__name__, self.__class__.__name__)

    def modify_pickup(self, request: Serializable[T]) -> Deserializable[S]:
        raise MethodNotSupportedError(self.__class__.modify_pickup.__name__, self.__class__.__name__)

    def cancel_pickup(self, request: Serializable[T]) -> Deserializable[S]:
        raise MethodNotSupportedError(self.__class__.cancel_pickup.__name__, self.__class__.__name__)
