import gzip
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
            data=lib.to_json(
                provider_utils.process_request(
                    self.settings, request.serialize(), "rates"
                )
            ),
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
            data=lib.to_json(
                provider_utils.process_request(
                    self.settings, request.serialize(), "tracking"
                )
            ),
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
        requests = request.serialize()
        responses = [
            lib.request(
                url=f"{self.settings.server_url}/ship/v1/shipments",
                data=lib.to_json(
                    provider_utils.process_request(
                        self.settings, requests[0], "shipments", request.ctx
                    )
                ),
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
        ]
        master_id = (
            lib.to_dict(responses[0])
            .get("output", {})
            .get("transactionShipments", [{}])[0]
            .get("masterTrackingNumber")
        )

        if len(requests) > 1 and master_id is not None:
            responses += lib.run_asynchronously(
                lambda _: lib.request(
                    url=f"{self.settings.server_url}/ship/v1/shipments",
                    data=(
                        lib.to_json(
                            provider_utils.process_request(
                                self.settings,
                                _,
                                "shipments",
                            )
                        )
                        .replace("[MASTER_ID_TYPE]", master_id.TrackingIdType)
                        .replace("[MASTER_TRACKING_ID]", master_id.TrackingNumber)
                    ),
                    trace=self.trace_as("json"),
                    method="POST",
                    headers={
                        "x-locale": "en_US",
                        "content-type": "application/json",
                        "authorization": f"Bearer {self.settings.access_token}",
                    },
                    decoder=provider_utils.parse_response,
                    on_error=lambda b: provider_utils.parse_response(b.read()),
                ),
                requests[1:],
            )

        return lib.Deserializable(
            responses,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/ship/v1/shipments/cancel",
            data=lib.to_json(
                provider_utils.process_request(
                    self.settings, request.serialize(), "cancel"
                )
            ),
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
