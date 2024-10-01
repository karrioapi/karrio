import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.fedex.utils as provider_utils
import karrio.mappers.fedex.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/rate/v1/rates/quotes",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/track/v1/trackingnumbers",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.track_access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        responses = lib.request(
            url=f"{self.settings.server_url}/ship/v1/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(responses, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/ship/v1/shipments/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)

    def upload_document(self, requests: lib.Serializable) -> lib.Deserializable:
        response = lib.run_asynchronously(
            lambda _: lib.request(
                url=(
                    "https://documentapitest.prod.fedex.com/sandbox/documents/v1/etds/upload"
                    if self.settings.test_mode
                    else "https://documentapi.prod.fedex.com/documents/v1/etds/upload"
                ),
                data=urllib.parse.urlencode(_),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "content-Type": "multipart/form-data",
                    "authorization": f"Bearer {self.settings.access_token}",
                },
            ),
            requests.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v1/pickups",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self.cancel_pickup(lib.Serializable(request.ctx["cancel"]))
        confirmation = response.deserialize().get("output") or {}

        if confirmation.get("pickupConfirmationCode") is not None:
            return self.schedule_pickup(request)

        return response

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v1/pickups/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)
