"""Karrio Teleship client proxy."""

import datetime
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.providers.teleship.error as provider_error
import karrio.mappers.teleship.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Retrieve access token using thread-safe token manager.

        Returns the cached token if available and not expired,
        otherwise fetches a new token from the OAuth endpoint.
        """
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
                seconds=float(response.get("expiresIn", 0))
            )

            return {**response, "expiry": lib.fdatetime(expiry)}

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="accessToken",
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()

        responses = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/api/rates/quotes",
                data=lib.to_json(payload),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()

        responses = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/api/shipments/labels",
                data=lib.to_json(payload),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        shipment_id = request.serialize().get("shipmentId")

        response = lib.request(
            url=f"{self.settings.server_url}/api/shipments/labels/{shipment_id}/void",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate(request).deserialize()

        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/api/tracking/{tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
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

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()

        response = lib.request(
            url=f"{self.settings.server_url}/api/pickups",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        pickup_id = request.serialize().get("pickupId")

        response = lib.request(
            url=f"{self.settings.server_url}/api/pickups/{pickup_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()

        response = lib.request(
            url=f"{self.settings.server_url}/api/manifests",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def calculate_duties(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()

        response = lib.request(
            url=f"{self.settings.server_url}/api/trade-engine/duties-taxes",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def register_webhook(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()

        response = lib.request(
            url=f"{self.settings.server_url}/api/webhooks",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def deregister_webhook(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        webhook_id = request.serialize().get("webhookId")

        response = lib.request(
            url=f"{self.settings.server_url}/api/webhooks/{webhook_id}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        # DELETE returns 204 No Content on success - handle empty response
        return lib.Deserializable(
            response,
            lambda r: lib.to_dict(r) if r and r.strip() else {},
        )
