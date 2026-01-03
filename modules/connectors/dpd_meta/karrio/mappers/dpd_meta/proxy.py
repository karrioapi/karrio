"""Karrio DPD Group client proxy."""

import datetime
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.providers.dpd_meta.error as provider_error
import karrio.mappers.dpd_meta.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve access token using thread-safe token manager.

        DPD META-API login uses custom headers for authentication.
        Depending on account setup, credentials can be provided either as:
        - X-DPD-LOGIN + X-DPD-PASSWORD + X-DPD-BUCODE
        - X-DPD-CLIENTID + X-DPD-CLIENTSECRET + X-DPD-BUCODE
        """
        has_user_pass = any([self.settings.dpd_login, self.settings.dpd_password])
        has_client_creds = any(
            [self.settings.dpd_client_id, self.settings.dpd_client_secret]
        )

        # Build cache key
        identity = (
            f"u:{self.settings.dpd_login}"
            if has_user_pass
            else f"c:{self.settings.dpd_client_id}"
        )
        env = "test" if self.settings.test_mode else "prod"
        cache_key = (
            f"{self.settings.carrier_name}|{identity}|{self.settings.dpd_bucode}|{env}"
        )

        def get_token():
            # Build headers using lib.to_dict to filter None values
            headers = lib.to_dict(
                {
                    "X-DPD-BUCODE": self.settings.dpd_bucode,
                    "X-DPD-LOGIN": self.settings.dpd_login if has_user_pass else None,
                    "X-DPD-PASSWORD": (
                        self.settings.dpd_password if has_user_pass else None
                    ),
                    "X-DPD-CLIENTID": (
                        self.settings.dpd_client_id if has_client_creds else None
                    ),
                    "X-DPD-CLIENTSECRET": (
                        self.settings.dpd_client_secret if has_client_creds else None
                    ),
                }
            )

            response = lib.request_with_response(
                url=f"{self.settings.server_url}/login",
                trace=self.trace_as("json"),
                method="POST",
                headers=headers,
            )

            if response.is_error:
                error_data = lib.to_dict_safe(response.content)
                messages = provider_error.parse_error_response(
                    error_data, self.settings
                )

                if any(messages):
                    raise errors.ParsedMessagesError(messages=messages)

                raise errors.ShippingSDKError(
                    f"DPD login failed: HTTP {response.status_code} | {response.content}"
                )

            # Extract token from response headers
            token = response.get_header("X-DPD-TOKEN")

            if not token:
                raise errors.ShippingSDKError(
                    f"DPD login succeeded but no token in headers. "
                    f"Headers: {response.headers}"
                )

            # Token is valid for 24 hours according to DPD docs
            expiry = datetime.datetime.now() + datetime.timedelta(hours=24)

            return {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": 86400,
                "expiry": lib.fdatetime(expiry),
            }

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
        )

        return lib.Deserializable(token.get_state())

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a shipment with DPD META-API.

        POST /shipping/v1/shipment
        """
        access_token = self.authenticate().deserialize()
        label_format = request.ctx.get("label_format", "PDF")

        response = lib.request(
            url=f"{self.settings.server_url}/shipment?LabelPrintFormat={label_format}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Schedule a pickup with DPD META-API.

        POST /shipping/v1/pickupscheduling
        """
        access_token = self.authenticate().deserialize()

        response = lib.request(
            url=f"{self.settings.server_url}/pickupscheduling",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
