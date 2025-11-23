"""Karrio Teleship client proxy."""

import datetime
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.providers.teleship.error as provider_error
import karrio.mappers.teleship.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/rates/quotes",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
                **(
                    {"x-account-id": self.settings.connection_config.account_id.state}
                    if self.settings.connection_config.account_id.state
                    else {}
                ),
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/shipments/labels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
                **(
                    {"x-account-id": self.settings.connection_config.account_id.state}
                    if self.settings.connection_config.account_id.state
                    else {}
                ),
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        shipment_id = request.serialize().get("shipmentId")

        response = lib.request(
            url=f"{self.settings.server_url}/api/shipments/labels/{shipment_id}/void",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Bearer {self.settings.access_token}",
                **(
                    {"x-account-id": self.settings.connection_config.account_id.state}
                    if self.settings.connection_config.account_id.state
                    else {}
                ),
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/api/tracking/{tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Authorization": f"Bearer {self.settings.access_token}",
                    **(
                        {
                            "x-account-id": self.settings.connection_config.account_id.state
                        }
                        if self.settings.connection_config.account_id.state
                        else {}
                    ),
                },
            )

        # Use concurrent requests for multiple tracking numbers
        responses = lib.run_concurently(_get_tracking, request.serialize())

        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )

    def authenticate(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        """Retrieve access token using thread-safe token manager"""
        cache_key = f"{self.settings.carrier_name}|{self.settings.client_id}|{self.settings.client_secret}"

        def get_token():
            response = lib.request(
                url=f"{self.settings.server_url}/oauth/token",
                method="POST",
                headers={"content-Type": "application/x-www-form-urlencoded"},
                data=lib.to_query_string(
                    dict(
                        grant_type="client_credentials",
                        clientId=self.settings.client_id,
                        clientSecret=self.settings.client_secret,
                    )
                ),
                decoder=lib.to_dict,
            )

            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages)

            expiry = datetime.datetime.now() + datetime.timedelta(
                seconds=float(response.get("expires_in", 0))
            )

            return {**response, "expiry": lib.fdatetime(expiry)}

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="accessToken",
        )

        return lib.Deserializable(token.get_state())
