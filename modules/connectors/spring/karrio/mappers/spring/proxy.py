"""Karrio Spring client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.spring.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Content-Type": "text/json"},
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Content-Type": "text/json"},
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Content-Type": "text/json"},
        )

        return lib.Deserializable(response, lib.to_dict)
