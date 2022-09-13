"""Karrio UPS Freight client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.ups_freight.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request(
            lib.Serializable(request.serialize(), lib.to_json),
            path="/ship/v1/freight/shipments/ground",
            method="POST",
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request(
            lib.Serializable(request.serialize(), lib.to_json),
            path="/ship/v1/freight/shipments/ground",
            method="POST",
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request(
            lib.Serializable(request.serialize(), lib.to_json),
            path="/ship/v1/freight/pickups",
            method="POST",
        )

        return lib.Deserializable(response, lib.to_dict)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        requests = request.serialize()
        cancel_response = self.cancel_pickup(requests["cancel"])
        cancel: dict = (
            cancel_response.deserialize().get("FreightCancelPickupResponse") or {}
        )

        # abort if cancellation request fails.
        if cancel.get("FreightCancelStatus") != "1":
            return cancel_response

        return self.schedule_pickup(requests["create"])

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request(
            path="/ship/v1/freight/pickups",
            headers=request.serialize(),
            method="DELETE",
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(
        self, request: lib.Serializable[typing.List[str]]
    ) -> lib.Deserializable[typing.List[typing.Tuple[str, dict]]]:
        """
        get_tracking makes background requests for each tracking number
        """

        def _get_tracking(tracking_number: str):
            return tracking_number, self._send_request(
                path=f"/track/v1/details/{tracking_number}",
                method="GET",
            )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_concurently(
            _get_tracking, request.serialize()
        )
        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )

    def upload_document(self, request: lib.Serializable) -> lib.Deserializable:
        url = (
            "https://wwwcie.ups.com/rest/PaperlessDocumentAPI"
            if self.settings.test_mode
            else "https://filexfer.ups.com/rest/PaperlessDocumentAPI"
        )

        def _upload(data: dict):
            name = data["UploadRequest"]["UserCreatedForm"]["UserCreatedFormFileName"]
            return name, self._send_request(
                lib.Serializable(data, lib.to_json),
                url=url,
            )

        responses = lib.run_concurently(_upload, request.serialize())
        return lib.Deserializable(
            responses, lambda values: [(n, lib.to_dict(r)) for n, r in values]
        )

    def _send_request(
        self,
        request: lib.Serializable = None,
        method: str = None,
        path: str = None,
        url: str = None,
        headers: dict = None,
    ) -> str:
        data = dict(data=request.serialize()) if request is not None else {}

        return lib.request(
            url=(url or f"{self.settings.server_url}{path}"),
            trace=self.trace_as("json"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "AccessLicenseNumber": self.settings.access_license_number,
                "Username": self.settings.username,
                "Password": self.settings.password,
                "transId": "",
                "transactionSrc": "",
                **(headers or {}),
            },
            method=(method or "POST"),
            **data,
        )
