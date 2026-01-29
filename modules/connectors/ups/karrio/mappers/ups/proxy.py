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
        """Authenticate and return access_token wrapped in Deserializable."""
        return lib.Deserializable(self.get_token())

    def get_token(self) -> str:
        """Retrieve access_token using client credentials, with caching."""
        cache_key = f"{self.settings.carrier_name}|{self.settings.client_id}|{self.settings.client_secret}"

        def fetch_token():
            merchant_id = self.settings.connection_config.merchant_id.state
            result = lib.request(
                url=f"{self.settings.server_url}/security/v1/oauth/token",
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "authorization": f"Basic {self.settings.authorization}",
                    "content-Type": "application/x-www-form-urlencoded",
                    **({"x-merchant-id": merchant_id} if merchant_id else {}),
                },
                data="grant_type=client_credentials",
            )
            response = lib.to_dict(result)
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages=messages)

            expiry = datetime.datetime.fromtimestamp(
                float(response.get("issued_at")) / 1000
            ) + datetime.timedelta(seconds=float(response.get("expires_in", 0)))
            return {**response, "expiry": lib.fdatetime(expiry)}

        return self.settings.connection_cache.thread_safe(
            refresh_func=fetch_token,
            cache_key=cache_key,
            buffer_minutes=30,
        ).get_state()

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/api/rating/v2409/Shop?additionalinfo=timeintransit",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "authorization": f"Bearer {self.get_token()}",
                "content-Type": "application/json",
            },
            data=lib.to_json(request.serialize()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/api/shipments/v2409/ship",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "authorization": f"Bearer {self.get_token()}",
                "content-Type": "application/json",
            },
            data=lib.to_json(request.serialize()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        shipment_id = request.serialize().get("shipmentidentificationnumber")
        response = lib.request(
            url=f"{self.settings.server_url}/api/shipments/v2409/void/cancel/{shipment_id}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "authorization": f"Bearer {self.get_token()}",
                "content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[typing.List[typing.Tuple[str, dict]]]:
        locale = self.settings.connection_config.locale.state or "en_US"
        token = self.get_token()

        responses = lib.run_concurently(
            lambda tracking_number: (
                tracking_number,
                lib.request(
                    url=f"{self.settings.server_url}/api/track/v1/details/{tracking_number}?locale={locale}&returnSignature=true",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "authorization": f"Bearer {token}",
                        "content-Type": "application/json",
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda res: [(num, lib.to_dict(data)) for num, data in res if any(data.strip())],
        )

    def upload_document(self, request: lib.Serializable) -> lib.Deserializable:
        payload = request.serialize()
        shipper_number = payload["UploadRequest"]["ShipperNumber"]

        response = lib.request(
            url=f"{self.settings.server_url}/api/paperlessdocuments/v1/upload",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "authorization": f"Bearer {self.get_token()}",
                "content-Type": "application/json",
                "ShipperNumber": shipper_number,
            },
            data=lib.to_json(payload),
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/api/pickupcreation/v2409/pickup",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "authorization": f"Bearer {self.get_token()}",
                "content-Type": "application/json",
            },
            data=lib.to_json(request.serialize()),
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        payload = request.serialize()
        prn = payload.get("prn")
        cancel_by = payload.get("cancel_by", "02")

        response = lib.request(
            url=f"{self.settings.server_url}/api/shipments/v2409/pickup/{cancel_by}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "authorization": f"Bearer {self.get_token()}",
                "content-Type": "application/json",
                **({"Prn": prn} if prn else {}),
            },
        )

        return lib.Deserializable(response, lib.to_dict)
