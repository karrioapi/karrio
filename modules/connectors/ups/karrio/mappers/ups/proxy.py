import typing
import datetime
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.providers.ups.error as provider_error
from karrio.mappers.ups.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.settings.carrier_name}|{self.settings.client_id}|{self.settings.client_secret}"

        def get_token():
            merchant_id = self.settings.connection_config.merchant_id.state
            result = lib.request(
                url=f"{self.settings.server_url}/security/v1/oauth/token",
                trace=self.settings.trace_as("json"),
                data="grant_type=client_credentials",
                method="POST",
                headers={
                    "authorization": f"Basic {self.settings.authorization}",
                    "content-Type": "application/x-www-form-urlencoded",
                    **({"x-merchant-id": merchant_id} if merchant_id else {}),
                },
                max_retries=2,
            )
            response = lib.to_dict(result)
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages=messages)

            expiry = datetime.datetime.fromtimestamp(
                float(response.get("issued_at")) / 1000
            ) + datetime.timedelta(seconds=float(response.get("expires_in", 0)))
            return {**response, "expiry": lib.fdatetime(expiry)}

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
        )

        return lib.Deserializable(token.get_state())

    def _send_request(
        self,
        path: str,
        request: lib.Serializable = None,
        method: str = "POST",
        headers: dict = None,
    ) -> str:
        try:
            access_token = self.authenticate().deserialize()

            return lib.request(
                url=f"{self.settings.server_url}{path}",
                trace=self.trace_as("json"),
                method=method,
                headers={
                    "transId": "x-trans-id",
                    "transactionSrc": "x-trans-src",
                    "content-Type": "application/json",
                    "authorization": f"Bearer {access_token}",
                    **(headers or {}),
                },
                **({"data": lib.to_json(request.serialize())} if request else {}),
            )
        except errors.ParsedMessagesError as e:
            return lib.to_json(
                {
                    "response": {
                        "errors": [
                            {
                                "code": "401",
                                "message": "Authentication failed",
                            }
                        ]
                    }
                }
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

        responses: typing.List[typing.Tuple[str, str]] = lib.run_concurently(
            lambda tracking_number: (
                tracking_number,
                self._send_request(
                    f"/api/track/v1/details/{tracking_number}?locale={locale}&returnSignature=true",
                    method="GET",
                ),
            ),
            request.serialize(),
        )
        return lib.Deserializable(
            responses,
            lambda res: [(_, lib.to_dict(__)) for _, __ in res if any(__.strip())],
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
