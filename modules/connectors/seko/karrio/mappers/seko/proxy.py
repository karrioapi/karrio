"""Karrio SEKO Logistics client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.seko.utils as provider_utils
import karrio.mappers.seko.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/ratesqueryv1/availablerates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "access_key": f"{self.settings.access_key}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/labels/printshipment",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "access_key": f"{self.settings.access_key}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/labels/delete",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "access_key": f"{self.settings.access_key}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(
            response,
            lib.to_dict,
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/labels/statusv2",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "access_key": f"{self.settings.access_key}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v2/publishmanifestv4",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "access_key": f"{self.settings.access_key}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)
