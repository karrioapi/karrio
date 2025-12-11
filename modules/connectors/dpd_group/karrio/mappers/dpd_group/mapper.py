"""Karrio DPD Group client mapper."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.dpd_group as provider
import karrio.mappers.dpd_group.settings as provider_settings


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings
    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return provider.shipment_request(payload, self.settings)
    
    def create_pickup_request(
        self, payload: models.PickupRequest
    ) -> lib.Serializable:
        return provider.pickup_request(payload, self.settings)

    def parse_pickup_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return provider.parse_pickup_response(response, self.settings)
    
    def parse_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)
    
