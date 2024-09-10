"""Karrio SAPIENT client mapper."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.sapient as provider
import karrio.mappers.sapient.settings as provider_settings
import karrio.universal.providers.rating as universal_provider


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_rate_request(self, payload: models.RateRequest) -> lib.Serializable:
        return universal_provider.rate_request(payload, self.settings)

    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)

    def create_pickup_request(self, payload: models.PickupRequest) -> lib.Serializable:
        return provider.pickup_request(payload, self.settings)

    def create_pickup_update_request(
        self, payload: models.PickupUpdateRequest
    ) -> lib.Serializable:
        return provider.pickup_update_request(payload, self.settings)

    def create_cancel_pickup_request(
        self, payload: models.PickupCancelRequest
    ) -> lib.Serializable:
        return provider.pickup_cancel_request(payload, self.settings)

    def create_cancel_shipment_request(
        self, payload: models.ShipmentCancelRequest
    ) -> lib.Serializable[str]:
        return provider.shipment_cancel_request(payload, self.settings)

    def parse_cancel_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_pickup_cancel_response(response, self.settings)

    def parse_cancel_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_shipment_cancel_response(response, self.settings)

    def parse_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_response(response, self.settings)

    def parse_pickup_update_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_update_response(response, self.settings)

    def parse_rate_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
        return universal_provider.parse_rate_response(response, self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)
