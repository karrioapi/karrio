"""Karrio DPD Meta client proxy."""

import datetime

import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.lib as lib
import karrio.mappers.dpd_meta.settings as provider_settings
import karrio.providers.dpd_meta.error as provider_error
import karrio.providers.dpd_meta.location as provider_location
import karrio.providers.dpd_meta.units as provider_units
import karrio.providers.dpd_meta.utils as provider_utils
import karrio.schemas.dpd_meta.webapi as webapi
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    @property
    def _auth_cache_key(self) -> str:
        has_user_pass = any([self.settings.dpd_login, self.settings.dpd_password])
        identity = f"u:{self.settings.dpd_login}" if has_user_pass else f"c:{self.settings.dpd_client_id}"
        env = "test" if self.settings.test_mode else "prod"
        return f"{self.settings.carrier_name}|{identity}|{self.settings.dpd_bucode}|{env}"

    def _token_manager(self):
        """Construct the ``ThreadSafeTokenManager`` for the META `/login` token.

        DPD META-API login uses custom headers for authentication; depending on
        account setup, credentials are X-DPD-LOGIN + X-DPD-PASSWORD or
        X-DPD-CLIENTID + X-DPD-CLIENTSECRET, both alongside X-DPD-BUCODE.
        """
        has_user_pass = any([self.settings.dpd_login, self.settings.dpd_password])
        has_client_creds = any([self.settings.dpd_client_id, self.settings.dpd_client_secret])

        def get_token():
            # Build headers using lib.to_dict to filter None values
            headers = lib.to_dict(
                {
                    "X-DPD-BUCODE": self.settings.dpd_bucode,
                    "X-DPD-LOGIN": self.settings.dpd_login if has_user_pass else None,
                    "X-DPD-PASSWORD": (self.settings.dpd_password if has_user_pass else None),
                    "X-DPD-CLIENTID": (self.settings.dpd_client_id if has_client_creds else None),
                    "X-DPD-CLIENTSECRET": (self.settings.dpd_client_secret if has_client_creds else None),
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
                messages = provider_error.parse_error_response(error_data, self.settings)

                if any(messages):
                    raise errors.ParsedMessagesError(messages=messages)

                raise errors.ShippingSDKError(f"DPD login failed: HTTP {response.status_code} | {response.content}")

            # Extract token from response headers
            token = response.get_header("X-DPD-TOKEN")

            if not token:
                raise errors.ShippingSDKError(
                    f"DPD login succeeded but no token in headers. Headers: {response.headers}"
                )

            real_expiry = provider_utils.decode_token_expiry(token)
            expiry = real_expiry or (datetime.datetime.now() + datetime.timedelta(minutes=15))

            return {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": max(int((expiry - datetime.datetime.now()).total_seconds()), 0),
                "expiry": lib.fdatetime(expiry),
            }

        # buffer=5: a 30-min SEUR token has zero margin at 30; 24h token still refreshes early, 401 retry backstops skew.
        return self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=self._auth_cache_key,
            buffer_minutes=5,
        )

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve access token using the thread-safe token manager."""
        return lib.Deserializable(self._token_manager().get_state())

    @property
    def _ws_auth_cache_key(self) -> str:
        env = "test" if self.settings.test_mode else "prod"
        return f"{self.settings.carrier_name}|ws|{self.settings.dpd_login}|{env}"

    def authenticate_public_ws(self) -> tuple[str | None, list]:
        """Exchange the delisId + password for a public-WS authToken.

        The token is cached for a short window. Returns `(authToken, messages)` —
        `authToken` is None when login failed and `messages` carries the
        parsed faults.
        """
        delis_id = self.settings.dpd_login
        password = self.settings.dpd_password
        if not (delis_id and password):
            return None, []

        def get_token():
            response = lib.request(
                url=f"{self.settings.public_ws_url}/LoginService/V2_0",
                data=lib.envelope_serializer(
                    lib.create_envelope(
                        envelope_prefix="soapenv",
                        body_prefix="ns",
                        body_content=webapi.getAuth(
                            delisId=delis_id,
                            password=password,
                            messageLanguage="en_US",
                        ),
                    ),
                    namespace=(
                        'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                        'xmlns:ns="http://dpd.com/common/service/types/LoginService/2.0"'
                    ),
                    prefixes=dict(
                        Envelope="soapenv",
                        getAuth="ns",
                        delisId="",
                        password="",
                        messageLanguage="",
                    ),
                ),
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Content-Type": "text/xml; charset=utf-8",
                    "SOAPAction": "http://dpd.com/common/service/LoginService/2.0/getAuth",
                },
            )
            element = lib.to_element(response)
            login = lib.find_element("return", element, webapi.Login, first=True)
            token = getattr(login, "authToken", None) if login else None
            if not token:
                messages = provider_error.parse_soap_faults(element, self.settings)
                raise (
                    errors.ParsedMessagesError(messages=messages)
                    if messages
                    else errors.ShippingSDKError("DPD LoginService returned no authToken")
                )
            # V2_0 Login carries no real expiry; short window, correctness via LOGIN_5/6 reactive refresh.
            expiry = datetime.datetime.now() + datetime.timedelta(hours=2)
            return {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": int((expiry - datetime.datetime.now()).total_seconds()),
                "expiry": lib.fdatetime(expiry),
            }

        try:
            token = self.settings.connection_cache.thread_safe(
                refresh_func=get_token,
                cache_key=self._ws_auth_cache_key,
                buffer_minutes=30,
            )
            return token.get_state(), []
        except errors.ParsedMessagesError as exc:
            return None, list(exc.messages)

    def get_locations(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Search DPD locations via DepotDataService_V1_0.getDepotData.

        Backs the unified `karrio.Location` interface, and is reused internally
        for Shop2Shop / Shop2Home shipments and pickups — for reseller accounts
        the sendingDepot must be resolved per request from the sender / pickup
        postal code.

        `request` is the getDepotData envelope built by `location_request`,
        carrying an `[AUTH_TOKEN]` placeholder; its `ctx` holds the country +
        postal code. A resolved depot is cached 24h, so repeat origins skip
        both the LoginService and DepotDataService calls.
        """
        cache_key = f"{self.settings.carrier_name}|depot|{request.ctx.get('country')}|{request.ctx.get('zip_code')}"
        cached = self.settings.connection_cache.get(cache_key)
        if cached is not None:
            return lib.Deserializable(cached)

        response = ""
        for attempt in range(2):
            token, messages = self.authenticate_public_ws()
            if not token:
                return lib.Deserializable(messages, lambda _, msgs=messages: msgs)

            response = lib.request(
                url=f"{self.settings.public_ws_url}/DepotDataService/V1_0",
                data=request.serialize().replace("[AUTH_TOKEN]", token),
                trace=self.trace_as("xml"),
                method="POST",
                headers={
                    "Content-Type": "text/xml; charset=utf-8",
                    "SOAPAction": "http://dpd.com/common/service/DepotDataService/1.0/getDepotData",
                },
            )

            # Expired authToken (LOGIN_5/6) → drop the cached token and re-login once.
            # failsafe: a malformed/non-XML error body must fall through, not raise here.
            expired = (
                attempt == 0
                and "<depot>" not in (response or "")
                and lib.failsafe(
                    lambda resp=response: provider_error.is_ws_auth_expired(
                        provider_error.parse_soap_faults(lib.to_element(resp), self.settings)
                    )
                )
            )
            if expired:
                self.settings.connection_cache.delete(self._ws_auth_cache_key)
                continue
            break

        # Cache successful resolutions only (24h) — never cache a fault.
        if "<depot>" in (response or ""):
            self.settings.connection_cache.set(cache_key, response, timeout=86400)

        return lib.Deserializable(response)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a shipment with DPD META-API (POST /shipping/v1/shipment).

        Shop2Shop / Shop2Home requests carry a `[DEPOT]` placeholder for
        `sendingDepot` (stamped by `mapper.create_shipment_request`); the
        shipper's depot is resolved via the DepotDataService and substituted
        before posting — mandatory in reseller setups where the broker's
        auth-token depot is not the customer's depot.
        """
        label_format = request.ctx.get("label_format", "PDF")
        payload = request.serialize()

        if request.ctx.get("resolve_depot"):
            locations, _ = provider_location.parse_location_response(
                self.get_locations(request.ctx["depot_query"]), self.settings
            )
            payload = provider_units.inject_sending_depot(payload, locations, settings=self.settings, geo_routing=True)

        response = lib.authenticated_request(
            self._token_manager(),
            url=f"{self.settings.server_url}/shipment?LabelPrintFormat={label_format}",
            data=lib.to_json(payload),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-DPD-BUCODE": self.settings.dpd_bucode,
            },
            retry_on_statuses=(401, 403),
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Schedule a pickup with DPD META-API (POST /shipping/v1/pickupscheduling).

        For reseller accounts the pickup request carries a `[DEPOT]` placeholder
        for `sendingDepot`; the depot serving the pickup address is resolved via
        the DepotDataService and substituted before posting.
        """
        payload = request.serialize()

        if request.ctx.get("resolve_depot"):
            locations, _ = provider_location.parse_location_response(
                self.get_locations(request.ctx["depot_query"]), self.settings
            )
            payload = provider_units.inject_sending_depot(payload, locations, settings=self.settings, geo_routing=False)

        response = lib.authenticated_request(
            self._token_manager(),
            url=f"{self.settings.server_url}/pickupscheduling",
            data=lib.to_json(payload),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-DPD-BUCODE": self.settings.dpd_bucode,
            },
            retry_on_statuses=(401, 403),
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_return_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        return self.create_shipment(request)
