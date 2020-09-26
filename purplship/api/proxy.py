"""PurplShip Proxy base class definition module."""

import attr
from abc import ABC
from purplship.core.settings import Settings
from purplship.core.errors import MethodNotSupportedError
from purplship.core.utils.serializable import Deserializable, Serializable


@attr.s(auto_attribs=True)
class Proxy(ABC):
    """Unified Shipping API Proxy (Interface)
    """

    settings: Settings

    def get_rates(self, request: Serializable) -> Deserializable:
        raise MethodNotSupportedError(
            self.__class__.get_rates.__name__, self.settings.carrier_name
        )

    def get_tracking(self, request: Serializable) -> Deserializable:
        raise MethodNotSupportedError(
            self.__class__.get_tracking.__name__, self.settings.carrier_name
        )

    def create_shipment(self, request: Serializable) -> Deserializable:
        raise MethodNotSupportedError(
            self.__class__.create_shipment.__name__, self.settings.carrier_name
        )

    def request_pickup(self, request: Serializable) -> Deserializable:
        raise MethodNotSupportedError(
            self.__class__.request_pickup.__name__, self.settings.carrier_name
        )

    def update_pickup(self, request: Serializable) -> Deserializable:
        raise MethodNotSupportedError(
            self.__class__.update_pickup.__name__, self.settings.carrier_name
        )

    def modify_pickup(self, request: Serializable) -> Deserializable:
        raise MethodNotSupportedError(
            self.__class__.modify_pickup.__name__, self.settings.carrier_name
        )

    def cancel_pickup(self, request: Serializable) -> Deserializable:
        raise MethodNotSupportedError(
            self.__class__.cancel_pickup.__name__, self.settings.carrier_name
        )
