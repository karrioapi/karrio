"""Karrio Deutsche Post DHL client mapper."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.dpdhl as providers
from karrio.mappers.dpdhl.settings import Settings


class Mapper(mapper.Mapper):
    settings: Settings

    def create_rate_request(self, payload: models.RateRequest) -> lib.Serializable:
        return providers.rate_request(payload, self.settings)

    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return providers.tracking_request(payload, self.settings)

    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return providers.shipment_request(payload, self.settings)

    def create_cancel_shipment_request(
        self, payload: models.ShipmentCancelRequest
    ) -> lib.Serializable[str]:
        return providers.shipment_cancel_request(payload, self.settings)

    def parse_cancel_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return providers.parse_shipment_cancel_response(
            response.deserialize(), self.settings
        )

    def parse_rate_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
        return providers.parse_rate_response(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return providers.parse_shipment_response(response.deserialize(), self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        return providers.parse_tracking_response(response.deserialize(), self.settings)
