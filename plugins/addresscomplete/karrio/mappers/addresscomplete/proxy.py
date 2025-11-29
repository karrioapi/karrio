"""Karrio AddressComplete client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.addresscomplete.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def validate_address(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        """Validate an address using Canada Post AddressComplete API."""
        response = lib.request(
            url=f"{self.settings.server_url}/Find/2.1/json.ws",
            params=request.serialize(),
            trace=self.trace_as("json"),
            method="GET",
        )

        return lib.Deserializable(response, lib.to_dict)
