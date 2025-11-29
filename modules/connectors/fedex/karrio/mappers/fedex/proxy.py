import datetime
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.providers.fedex.utils as provider_utils
import karrio.providers.fedex.error as provider_error
import karrio.mappers.fedex.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/rate/v1/rates/quotes",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/track/v1/trackingnumbers",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate(request).deserialize()
        responses = lib.request(
            url=f"{self.settings.server_url}/ship/v1/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(responses, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/ship/v1/shipments/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)

    def upload_document(self, requests: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate(requests).deserialize()
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
                    "authorization": f"Bearer {access_token}",
                },
            ),
            requests.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v1/pickups",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self.cancel_pickup(lib.Serializable(request.ctx["cancel"]))
        confirmation = response.deserialize().get("output") or {}

        if confirmation.get("pickupConfirmationCode") is not None:
            return self.schedule_pickup(request)

        return response

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v1/pickups/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "x-locale": "en_US",
                "content-type": "application/json",
                "authorization": f"Bearer {access_token}",
            },
            decoder=provider_utils.parse_response,
            on_error=lambda b: provider_utils.parse_response(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def authenticate(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        """Retrieve the access_token using the api_key|secret_key pair
        or collect it from the cache if an unexpired access_token exist.
        """
        auth_type = lib.typed(
            dict(
                shipping_auth=dict(
                    required_values=[
                        self.settings.api_key,
                        self.settings.secret_key,
                        self.settings.account_number,
                    ],
                    cache_key=f"{self.settings.carrier_name}|{self.settings.api_key}|{self.settings.secret_key}",
                    required_fields="api_key, secret_key, account_number",
                    service="Rate, Ship and Other API requests.",
                    data=dict(
                        grant_type="client_credentials",
                        client_id=self.settings.api_key,
                        client_secret=self.settings.secret_key,
                    ),
                ),
                track_auth=dict(
                    required_values=[
                        self.settings.track_api_key,
                        self.settings.track_secret_key,
                    ],
                    cache_key=f"{self.settings.carrier_name}|{self.settings.track_api_key}|{self.settings.track_secret_key}",
                    required_fields="track_api_key, track_secret_key",
                    service="Track API requests.",
                    data=dict(
                        grant_type="client_credentials",
                        client_id=self.settings.track_api_key,
                        client_secret=self.settings.track_secret_key,
                    ),
                ),
            )[request.ctx.get("auth_type", "shipping_auth")]
        )

        if not all(auth_type.required_values):
            raise Exception(
                f"The {auth_type.required_fields} are required for {auth_type.service}."
            )

        def get_token():
            response = lib.request(
                url=f"{self.settings.server_url}/oauth/token",
                trace=self.settings.trace_as("json"),
                method="POST",
                headers={"content-Type": "application/x-www-form-urlencoded"},
                data=urllib.parse.urlencode(auth_type.data),
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
            cache_key=auth_type.cache_key,
            buffer_minutes=30,
        )

        return lib.Deserializable(token.get_state())
