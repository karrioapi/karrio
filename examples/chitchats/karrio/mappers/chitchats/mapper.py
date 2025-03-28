"""Karrio Chit Chats mapper."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.chitchats as provider
import karrio.mappers.chitchats.proxy as proxy
import karrio.mappers.chitchats.settings as settings


class Mapper:
    """Chit Chats mapper class for API operations."""

    def __init__(self, settings: settings.Settings) -> None:
        self.settings = settings
        self.proxy = proxy.Proxy(settings)

    """Get shipping rates."""

    def create_rate_request(self, payload: typing.Any) -> lib.Serializable:
        return provider.rate_request(payload, self.settings)

    def parse_rate_response(self, response: lib.Deserializable[dict]) -> tuple[list[models.RateDetails], list[models.Message]]:
        rates, messages = provider.parse_rate_response(response, self.settings)
        return rates, messages

    """Create a shipment and buy postage."""

    def create_shipment_request(self, payload: typing.Any) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)

    def parse_shipment_response(self, response: lib.Deserializable[dict]) -> tuple[models.ShipmentDetails, list[models.Message]]:
        details, messages = provider.parse_shipment_response(response, self.settings)
        return details, messages

    """Buy postage for an existing shipment."""

    def create_shipment_buy_request(self, payload: typing.Any) -> lib.Serializable:
        return provider.shipment_buy_request(payload, self.settings)

    def parse_shipment_buy_response(self, response: lib.Deserializable[dict]) -> tuple[models.ShipmentDetails, list[models.Message]]:
        details, messages = provider.parse_shipment_buy_response(response, self.settings)
        return details, messages

    """Create a batch."""

    def create_batch_request(self, payload: typing.Any) -> lib.Serializable:
        return provider.batch_request(payload, self.settings)

    def parse_batch_response(self, response: lib.Deserializable[dict]) -> tuple[models.ConfirmationDetails, list[models.Message]]:
        details, messages = provider.parse_batch_response(response, self.settings)
        return details, messages

    """Add shipments to a batch."""

    def create_add_to_batch_request(self, payload: typing.Any) -> lib.Serializable:
        return provider.add_to_batch_request(payload, self.settings)

    def parse_add_to_batch_response(self, response: lib.Deserializable[dict]) -> tuple[models.ConfirmationDetails, list[models.Message]]:
        details, messages = provider.parse_add_to_batch_response(response, self.settings)
        return details, messages 
