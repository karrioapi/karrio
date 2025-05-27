import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.mappers.ups.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings

    def _send_request(
        self,
        path: str,
        request: lib.Serializable = None,
        method: str = "POST",
        headers: dict = None,
    ) -> str:
        return lib.request(
            url=f"{self.settings.server_url}{path}",
            trace=self.trace_as("json"),
            method=method,
            headers={
                "transId": "x-trans-id",
                "transactionSrc": "x-trans-src",
                "content-Type": "application/json",
                "authorization": f"Bearer {self.settings.access_token}",
                **(headers or {}),
            },
            **({"data": lib.to_json(request.serialize())} if request else {}),
        )

    def get_rates(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable:
        response = self._send_request(
            "/api/rating/v2409/Shop?additionalinfo=timeintransit",
            request,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def create_shipment(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable:
        response = self._send_request(
            "/api/shipments/v2409/ship",
            request,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable:
        response = self._send_request(
            f"/api/shipments/v2409/void/cancel/{request.serialize().get('shipmentidentificationnumber')}",
            method="DELETE",
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(
        self, request: lib.Serializable
    ) -> lib.Deserializable[typing.List[typing.Tuple[str, dict]]]:
        """get_tracking makes background requests for each tracking number"""
        locale = self.settings.connection_config.locale.state or "en_US"

        def _get_tracking(tracking_number: str):
            return tracking_number, self._send_request(
                f"/api/track/v1/details/{tracking_number}?locale={locale}&returnSignature=true",
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

    def upload_document(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable:
        payload = request.serialize()
        shipper_number = payload["UploadRequest"]["ShipperNumber"]

        response = self._send_request(
            f"/api/paperlessdocuments/v1/upload",
            headers=dict(ShipperNumber=shipper_number),
        )

        return lib.Deserializable(response, lib.to_dict)
