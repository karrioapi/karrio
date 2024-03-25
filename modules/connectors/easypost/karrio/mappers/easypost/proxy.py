import typing
import karrio.lib as lib
import karrio.api.proxy as base
import karrio.mappers.easypost.settings as provider_settings


class Proxy(base.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            path="/shipments",
            request=lib.Serializable(request.serialize(), lib.to_json),
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        payload = request.serialize()

        def create(request) -> str:
            response = lib.to_dict(
                self._send_request(
                    path="/shipments", request=lib.Serializable(request, lib.to_json)
                )
            )

            if "error" in response:
                return response

            # retrieve rate with the selected service.
            rate_id = next(
                (
                    rate["id"]
                    for rate in response.get("rates", [])
                    if rate["service"] == payload["service"]
                ),
                None,
            )
            data = lib.to_dict(
                {
                    "rate": {"id": rate_id},
                    "insurance": payload.get("insurance"),
                }
            )

            if rate_id is None:
                raise Exception("No rate found for the given service.")

            return self._send_request(
                path=f"/shipments/{response['id']}/buy",
                request=lib.Serializable(data, lib.to_json),
            )

        response = create(payload["data"])
        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(path=f"/shipments/{request.serialize()}/refund")

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        track = lambda request: (
            request["tracking_code"],
            self._send_request(
                **(
                    dict(
                        path="/trackers", request=lib.Serializable(request, lib.to_json)
                    )
                    if request.get("tracker_id") is None
                    else dict(path=f"/trackers/{request['tracker_id']}", method="GET")
                )
            ),
        )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            track, requests.serialize()
        )
        return lib.Deserializable(
            responses,
            lambda res: [(key, lib.to_dict(response)) for key, response in res],
        )

    def _send_request(
        self, path: str, request: lib.Serializable = None, method: str = "POST"
    ) -> str:
        data: dict = dict(data=request.serialize()) if request is not None else dict()
        return lib.request(
            **{
                "url": f"{self.settings.server_url}{path}",
                "trace": self.trace_as("json"),
                "method": method,
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
                **data,
            }
        )
