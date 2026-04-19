"""Karrio DHL Express client mapper."""

import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.lib as lib
import karrio.mappers.dhl_express.settings as provider_settings
import karrio.providers.dhl_express as provider


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_address_validation_request(self, payload: models.AddressValidationRequest) -> lib.Serializable:
        return provider.address_validation_request(payload, self.settings)

    def create_rate_request(self, payload: models.RateRequest) -> lib.Serializable:
        return provider.rate_request(payload, self.settings)

    def create_tracking_request(self, payload: models.TrackingRequest) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)

    def create_shipment_request(self, payload: models.ShipmentRequest) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)

    def create_pickup_request(self, payload: models.PickupRequest) -> lib.Serializable:
        return provider.pickup_request(payload, self.settings)

    def create_pickup_update_request(self, payload: models.PickupUpdateRequest) -> lib.Serializable:
        return provider.pickup_update_request(payload, self.settings)

    def create_cancel_pickup_request(self, payload: models.PickupCancelRequest) -> lib.Serializable:
        return provider.pickup_cancel_request(payload, self.settings)

    def create_document_upload_request(self, payload: models.DocumentUploadRequest) -> lib.Serializable:
        return super().create_document_upload_request(payload)

    def parse_address_validation_response(
        self, response: lib.Deserializable
    ) -> tuple[models.AddressValidationDetails, list[models.Message]]:
        return provider.parse_address_validation_response(response, self.settings)

    def parse_cancel_pickup_response(
        self, response: lib.Deserializable
    ) -> tuple[models.ConfirmationDetails, list[models.Message]]:
        return provider.parse_pickup_cancel_response(response, self.settings)

    def parse_pickup_response(self, response: lib.Deserializable) -> tuple[models.PickupDetails, list[models.Message]]:
        return provider.parse_pickup_response(response, self.settings)

    def parse_pickup_update_response(
        self, response: lib.Deserializable
    ) -> tuple[models.PickupDetails, list[models.Message]]:
        return provider.parse_pickup_update_response(response, self.settings)

    def parse_rate_response(
        self, response: lib.Deserializable
    ) -> tuple[list[models.RateDetails], list[models.Message]]:
        return provider.parse_rate_response(response, self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable
    ) -> tuple[models.ShipmentDetails, list[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable
    ) -> tuple[list[models.TrackingDetails], list[models.Message]]:
        return provider.parse_tracking_response(response, self.settings)

    def create_return_shipment_request(self, payload: models.ShipmentRequest) -> lib.Serializable:
        return provider.return_shipment_request(payload, self.settings)

    def parse_return_shipment_response(
        self, response: lib.Deserializable
    ) -> tuple[models.ShipmentDetails, list[models.Message]]:
        return provider.parse_return_shipment_response(response, self.settings)
