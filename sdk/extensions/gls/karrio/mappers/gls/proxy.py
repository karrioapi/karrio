
"""Karrio GLS client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.gls.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, lib.to_dict)
    