"""Karrio Teleship client mapper."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.teleship as provider
import karrio.mappers.teleship.settings as provider_settings


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_rate_request(
        self, payload: models.RateRequest
    ) -> lib.Serializable:
        return provider.rate_request(payload, self.settings)
    
    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)
    
    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)
    
    def create_cancel_shipment_request(
        self, payload: models.ShipmentCancelRequest
    ) -> lib.Serializable[str]:
        return provider.shipment_cancel_request(payload, self.settings)
    
    
    def parse_cancel_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_shipment_cancel_response(response, self.settings)
    
    def parse_rate_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
        return provider.parse_rate_response(response, self.settings)
    
    def parse_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)
    
    def parse_tracking_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        return provider.parse_tracking_response(response, self.settings)

    def create_pickup_request(
        self, payload: models.PickupRequest
    ) -> lib.Serializable:
        return provider.pickup_request(payload, self.settings)

    def create_cancel_pickup_request(
        self, payload: models.PickupCancelRequest
    ) -> lib.Serializable:
        return provider.cancel_pickup_request(payload, self.settings)

    def parse_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_response(response, self.settings)

    def parse_cancel_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_cancel_pickup_response(response, self.settings)

    def create_manifest_request(
        self, payload: models.ManifestRequest
    ) -> lib.Serializable:
        return provider.manifest_request(payload, self.settings)

    def parse_manifest_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
        return provider.parse_manifest_response(response, self.settings)

    def create_duties_calculation_request(
        self, payload: models.DutiesCalculationRequest
    ) -> lib.Serializable:
        return provider.duties_calculation_request(payload, self.settings)

    def parse_duties_calculation_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.DutiesCalculationDetails, typing.List[models.Message]]:
        return provider.parse_duties_calculation_response(response, self.settings)

    def create_webhook_registration_request(
        self, payload: models.WebhookRegistrationRequest
    ) -> lib.Serializable:
        return provider.webhook_registration_request(payload, self.settings)

    def parse_webhook_registration_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.WebhookRegistrationDetails, typing.List[models.Message]]:
        return provider.parse_webhook_registration_response(response, self.settings)

    def create_webhook_deregistration_request(
        self, payload: models.WebhookDeregistrationRequest
    ) -> lib.Serializable:
        return provider.webhook_deregistration_request(payload, self.settings)

    def parse_webhook_deregistration_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return provider.parse_webhook_deregistration_response(response, self.settings)
    
