"""Karrio SAPIENT client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.sapient.utils as provider_utils
import karrio.mappers.sapient.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v4/shipments/{request.ctx['carrier_code']}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
                "user-agent": "Karrio/1.0",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v4/shipments/status",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
                "user-agent": "Karrio/1.0",
            },
            on_ok=lambda _: '{"ok": true}',
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v4/collections/{request.ctx['carrier_code']}/{request.ctx['shipmentId']}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
                "user-agent": "Karrio/1.0",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self.cancel_pickup(lib.Serializable(request.ctx))

        if response.deserialize()["ok"]:
            response = self.schedule_pickup(request)

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/v4/collections/{payload['carrier_code']}/{payload['shipmentId']}/cancel",
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
                "user-agent": "Karrio/1.0",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)
