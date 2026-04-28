"""Karrio Google Geocoding client mapper."""

import karrio.api.mapper as mapper
import karrio.core.models as models
import karrio.lib as lib
import karrio.mappers.googlegeocoding.settings as provider_settings
import karrio.providers.googlegeocoding as provider


class Mapper(mapper.Mapper):
    settings: provider_settings.Settings

    def create_address_validation_request(self, payload: models.AddressValidationRequest) -> lib.Serializable:
        return provider.address_validation_request(payload, self.settings)

    def parse_address_validation_response(
        self, response: lib.Deserializable[dict]
    ) -> tuple[models.AddressValidationDetails, list[models.Message]]:
        return provider.parse_address_validation_response(response, self.settings)
