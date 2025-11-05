"""Karrio DPD Group mapper."""

from __future__ import annotations
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

    def create_shipment(
        self, payload: models.ShipmentRequest
    ) -> lib.Job[models.ShipmentDetails]:
        return lib.run_asynchronously(self._create_shipment)(payload)

    def _create_shipment(
        self, payload: models.ShipmentRequest
    ) -> lib.Job[models.ShipmentDetails]:
        request = self.create_shipment_request(payload)
        response = self.proxy.create_shipment(request)
        return self.parse_shipment_response(response)

    def parse_shipment_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.Optional[models.ShipmentDetails], typing.List[models.Message]]:
        return provider.parse_shipment_response(response, self.settings)

    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)

    def get_tracking(
        self, payload: models.TrackingRequest
    ) -> lib.Job[typing.List[models.TrackingDetails]]:
        return lib.run_asynchronously(self._get_tracking)(payload)

    def _get_tracking(
        self, payload: models.TrackingRequest
    ) -> lib.Job[typing.List[models.TrackingDetails]]:
        request = self.create_tracking_request(payload)
        response = self.proxy.get_tracking(request)
        return self.parse_tracking_response(response)

    def parse_tracking_response(
        self, response: lib.Deserializable[str]
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        # Handle multiple tracking responses
        tracking_results = []
        all_messages = []

        responses = response.deserialize()
        if not isinstance(responses, list):
            responses = [(None, responses)]

        for tracking_number, tracking_response in responses:
            details, messages = provider.parse_tracking_response(
                lib.Deserializable(tracking_response, lambda r: r), self.settings
            )
            tracking_results.extend(details)
            all_messages.extend(messages)

        return tracking_results, all_messages
