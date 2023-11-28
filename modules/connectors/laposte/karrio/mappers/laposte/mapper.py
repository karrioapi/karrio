"""Karrio La Poste client mapper."""

import typing
import karrio.lib as lib
import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.providers.laposte as provider
import karrio.mappers.laposte.settings as provider_settings


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return provider.tracking_request(payload, self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        return provider.parse_tracking_response(response, self.settings)
