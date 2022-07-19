"""Karrio Proxy abstract class definition module."""

import attr
import functools
from abc import ABC
from karrio.core.settings import Settings
from karrio.core.errors import MethodNotSupportedError
from karrio.core.utils import Deserializable, Serializable, Tracer


@attr.s(auto_attribs=True)
class Proxy(ABC):
    """Unified Shipping API Proxy (Interface)"""

    settings: Settings
    tracer: Tracer = attr.field(factory=Tracer)

    def trace(self, *args, **kwargs):
        return self.tracer.with_metadata(dict(connection=self.settings))(
            *args, **kwargs
        )

    def trace_as(self, format: str):
        return functools.partial(self.trace, format=format)

    def get_rates(self, request: Serializable) -> Deserializable:
        """Send one or many request(s) to get shipment rates from a carrier webservice

        Args:
            request (Serializable): a carrier specific serializable request data type

        Returns:
            Deserializable: a deserializable rate response (xml, json, text...)

        Raises:
           Deserializable: a deserializable rate response (xml, json, text...)
        """
        raise MethodNotSupportedError(
            self.__class__.get_rates.__name__, self.settings.carrier_name
        )

    def get_tracking(self, request: Serializable) -> Deserializable:
        """Send one or many request(s) to get tracking details from a carrier webservice

        Args:
            request (Serializable): a carrier specific serializable request data type

        Returns:
           Deserializable: a deserializable rate response (xml, json, text...)

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise MethodNotSupportedError(
            self.__class__.get_tracking.__name__, self.settings.carrier_name
        )

    def create_shipment(self, request: Serializable) -> Deserializable:
        """Send one or many request(s) to create a shipment from a carrier webservice

        Args:
            request (Serializable): a carrier specific serializable request data type

        Returns:
            Deserializable: a deserializable rate response (xml, json, text...)

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise MethodNotSupportedError(
            self.__class__.create_shipment.__name__, self.settings.carrier_name
        )

    def cancel_shipment(self, request: Serializable) -> Deserializable:
        """Send one or many request(s) cancel a shipment from a carrier webservice

        Args:
            request (Serializable): a carrier specific serializable request data type

        Returns:
            Deserializable: a deserializable rate response (xml, json, text...)

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise MethodNotSupportedError(
            self.__class__.cancel_shipment.__name__, self.settings.carrier_name
        )

    def schedule_pickup(self, request: Serializable) -> Deserializable:
        """Send one or many request(s) to schedule pickup from a carrier webservice

        Args:
            request (Serializable): a carrier specific serializable request data type

        Returns:
            Deserializable: a deserializable rate response (xml, json, text...)

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise MethodNotSupportedError(
            self.__class__.schedule_pickup.__name__, self.settings.carrier_name
        )

    def modify_pickup(self, request: Serializable) -> Deserializable:
        """Send one or many request(s) to update a pickup from a carrier webservice

        Args:
            request (Serializable): a carrier specific serializable request data type

        Returns:
            Deserializable: a deserializable rate response (xml, json, text...)

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise MethodNotSupportedError(
            self.__class__.modify_pickup.__name__, self.settings.carrier_name
        )

    def cancel_pickup(self, request: Serializable) -> Deserializable:
        """Send one or many request(s) to cancel a pickup from a carrier webservice

        Args:
            request (Serializable): a carrier specific serializable request data type

        Returns:
            Deserializable: a deserializable rate response (xml, json, text...)

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise MethodNotSupportedError(
            self.__class__.cancel_pickup.__name__, self.settings.carrier_name
        )

    def validate_address(self, request: Serializable) -> Deserializable:
        """Send one or many request(s) to validated an address from a carrier webservice

        Args:
            request (Serializable): a carrier specific serializable request data type

        Returns:
            Deserializable: a deserializable rate response (xml, json, text...)

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise MethodNotSupportedError(
            self.__class__.validate_address.__name__, self.settings.carrier_name
        )
