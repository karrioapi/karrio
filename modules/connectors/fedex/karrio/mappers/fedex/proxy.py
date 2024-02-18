import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.mappers.fedex.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request("/rate", request)

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request("/track/v1/trackingnumbers", request)

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        requests = request.serialize()
        responses = [self._send_request("/ship", lib.Serializable(requests[0]))]
        master_id = (
            lib.to_dict(responses[0])
            .get("output", {})
            .get("transactionShipments", [{}])[0]
            .get("masterTrackingNumber")
        )

        if len(requests) > 1 and master_id is not None:
            responses += lib.run_asynchronously(
                lambda _: self._send_request(
                    "/ship",
                    lib.Serializable(
                        request.replace(
                            "[MASTER_ID_TYPE]", master_id.TrackingIdType
                        ).replace("[MASTER_TRACKING_ID]", master_id.TrackingNumber),
                    ),
                ),
                requests[1:],
            )

        return lib.Deserializable(
            responses,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request("/ship", request)

        return lib.Deserializable(response, lib.to_dict)

    def upload_document(self, requests: lib.Serializable) -> lib.Deserializable:
        response = lib.run_asynchronously(
            lambda _: self._send_request(
                url=(
                    "https://documentapitest.prod.fedex.com/sandbox/documents/v1/etds/upload"
                    if self.settings.test_mode
                    else "https://documentapi.prod.fedex.com/documents/v1/etds/upload"
                ),
                request=lib.Serializable(_, urllib.parse.urlencode),
                headers={"content-Type": "multipart/form-data"},
            ),
            requests.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def _send_request(
        self,
        path: str = "/",
        request: lib.Serializable = None,
        method: str = "POST",
        headers: dict = None,
        url: str = None,
    ) -> str:
        return lib.request(
            url=url or f"{self.settings.server_url}{path}",
            trace=self.trace_as("json"),
            method=method,
            headers={
                "content-Type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
                "x-locale": self.settings.connection_config.locale.state or "en_US",
                **(headers or {}),
            },
            **({"data": lib.to_json(request.serialize())} if request else {}),
        )
