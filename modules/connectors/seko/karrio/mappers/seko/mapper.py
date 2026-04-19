"""Karrio SEKO Logistics client mapper."""

import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.lib as lib
import karrio.mappers.seko.settings as provider_settings
import karrio.providers.seko as provider


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_rate_request(self, payload: models.RateRequest) -> lib.Serializable:
        return provider.rate_request(payload, self.settings)

    def create_tracking_request(self, payload: models.TrackingRequest) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)

    def create_shipment_request(self, payload: models.ShipmentRequest) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)

    def create_cancel_shipment_request(self, payload: models.ShipmentCancelRequest) -> lib.Serializable[str]:
        return provider.shipment_cancel_request(payload, self.settings)

    def create_manifest_request(self, payload: models.ManifestRequest) -> lib.Serializable:
        return provider.manifest_request(payload, self.settings)

    def parse_cancel_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> tuple[models.ConfirmationDetails, list[models.Message]]:
        return provider.parse_shipment_cancel_response(response, self.settings)

    def parse_rate_response(
        self, response: lib.Deserializable[str]
    ) -> tuple[list[models.RateDetails], list[models.Message]]:
        return provider.parse_rate_response(response, self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> tuple[models.ShipmentDetails, list[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable[str]
    ) -> tuple[list[models.TrackingDetails], list[models.Message]]:
        return provider.parse_tracking_response(response, self.settings)

    def parse_manifest_response(
        self, response: lib.Deserializable[str]
    ) -> tuple[models.ManifestDetails, list[models.Message]]:
        return provider.parse_manifest_response(response, self.settings)
