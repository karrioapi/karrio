"""Karrio La Poste client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.laposte.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        idships = ",".join(request.serialize())
        response = lib.request(
            url=f"{self.settings.server_url}/idships/{idships}?lang={self.settings.lang}",
            trace=self.trace_as("json"),
            headers={
                "accept": "application/json",
                "X-Okapi-Key": self.settings.api_key,
            },
            method="GET",
        )

        return lib.Deserializable(response, lib.to_dict)
