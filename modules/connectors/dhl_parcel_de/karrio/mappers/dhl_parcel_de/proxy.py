"""Karrio DHL Germany client proxy."""

import base64
import datetime
import urllib.parse

import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.lib as lib
import karrio.mappers.dhl_parcel_de.settings as provider_settings
import karrio.providers.dhl_parcel_de.error as provider_error
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    @property
    def _auth_cache_key(self) -> str:
        return f"{self.settings.carrier_name}|{self.settings.connection_client_id}|{self.settings.connection_client_secret}"

    def _token_manager(self):
        """Construct the ``ThreadSafeTokenManager`` for this connection.

        The manager is cheap to build — it's a thin wrapper around the cache —
        so we re-instantiate per call rather than holding it as state.
        """

        def get_token():
            response = lib.request(
                url=f"{self.settings.token_server_url}/token",
                trace=self.settings.trace_as("json"),
                data=lib.to_query_string(
                    dict(
                        grant_type="password",
                        username=self.settings.connection_username,
                        password=self.settings.connection_password,
                        client_id=self.settings.connection_client_id,
                        client_secret=self.settings.connection_client_secret,
                    )
                ),
                method="POST",
                headers={
                    "content-Type": "application/x-www-form-urlencoded",
                },
                decoder=lib.to_dict,
                on_error=lib.error_decoder,
                max_retries=2,
            )
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages=messages)

            expiry = datetime.datetime.now() + datetime.timedelta(seconds=int(response.get("expires_in", 0)))
            return {**response, "expiry": lib.fdatetime(expiry)}

        # DHL Parcel DE tokens are issued for 8 h (expires_in=28800). Refresh
        # while there's still ≥ 1 h of validity so a slow label flow (queued
        # rate fetch + label create) can never run on a near-expiry token.
        return self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=self._auth_cache_key,
            buffer_minutes=60,
        )

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        return lib.Deserializable(self._token_manager().get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        ctx = lib.to_dict(request.ctx) or {}
        meta = ctx.pop("_meta", {})  # Extract meta context for response parsing
        query = urllib.parse.urlencode(ctx)
        response = lib.authenticated_request(
            self._token_manager(),
            url=f"{self.settings.server_url}/v2/orders?{query}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Accept-Language": self.settings.language,
            },
        )

        return lib.Deserializable(response, lib.to_dict, meta)

    def create_return_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        ctx = lib.to_dict(request.ctx) or {}
        query = urllib.parse.urlencode(ctx)
        response = lib.authenticated_request(
            self._token_manager(),
            url=f"{self.settings.returns_server_url}/orders?{query}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Accept-Language": self.settings.language,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = lib.authenticated_request(
            self._token_manager(),
            url=f"{self.settings.server_url}/v2/orders?{query}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "content-type": "application/json",
                "Accept-Language": self.settings.language,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Fetch tracking info using DHL Parcel DE dedicated Tracking API.

        Uses XML request in query parameter with two-layer authentication:
        1. HTTP Basic Auth (API key:secret) for API gateway
        2. XML credentials (appname:password) in request for tracking service
        """
        # Build HTTP Basic Auth header
        auth_string = f"{self.settings.connection_client_id}:{self.settings.connection_client_secret}"
        basic_auth = base64.b64encode(auth_string.encode()).decode()

        responses: list[str] = lib.run_asynchronously(
            lambda xml_request: lib.request(
                url=f"{self.settings.tracking_server_url}?{urllib.parse.urlencode({'xml': xml_request})}",
                trace=self.trace_as("xml"),
                method="GET",
                headers={
                    "Accept": "application/xml",
                    "Authorization": f"Basic {basic_auth}",
                },
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda res: [lib.to_element(r) for r in res if r],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.authenticated_request(
            self._token_manager(),
            url=f"{self.settings.pickup_server_url}/orders",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Accept-Language": self.settings.language,
            },
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = lib.authenticated_request(
            self._token_manager(),
            url=f"{self.settings.pickup_server_url}/orders?{query}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "content-type": "application/json",
                "Accept-Language": self.settings.language,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
