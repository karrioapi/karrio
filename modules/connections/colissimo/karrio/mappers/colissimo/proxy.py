"""Karrio Colissimo client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.colissimo.utils as provider_utils
import karrio.mappers.colissimo.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/generateLabel",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Content-Type": "application/json;charset=UTF-8"},
        )

        return lib.Deserializable(response, provider_utils.parse_response, request.ctx)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        idships = ",".join(request.serialize())
        response = lib.request(
            url=f"{self.settings.laposte_server_url}/idships/{idships}?lang={self.settings.connection_config.lang.state or 'fr_FR'}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "accept": "application/json",
                "X-Okapi-Key": self.settings.laposte_api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
