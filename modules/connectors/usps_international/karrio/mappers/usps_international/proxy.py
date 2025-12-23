"""Karrio USPS International client proxy."""

import datetime
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.providers.usps_international.error as provider_error
import karrio.providers.usps_international.utils as provider_utils
import karrio.mappers.usps_international.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"access|{self.settings.carrier_name}|{self.settings.client_id}|{self.settings.client_secret}"

        def get_token():
            API_SCOPES = [
                "addresses",
                "international-prices",
                "subscriptions",
                "payments",
                "pickup",
                "tracking",
                "labels",
                "scan-forms",
                "companies",
                "service-delivery-standards",
                "locations",
                "international-labels",
                "prices",
                "shipments",
            ]
            result = lib.request(
                url=f"{self.settings.server_url}/oauth2/v3/token",
                trace=self.settings.trace_as("json"),
                method="POST",
                headers={"content-Type": "application/x-www-form-urlencoded"},
                data=lib.to_query_string(
                    dict(
                        grant_type="client_credentials",
                        client_id=self.settings.client_id,
                        client_secret=self.settings.client_secret,
                        scope=" ".join(API_SCOPES),
                    )
                ),
                max_retries=2,
            )

            response = lib.to_dict(result)
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
        )

        return lib.Deserializable(token.get_state())

    def get_payment_token(self, _=None) -> lib.Deserializable[str]:
        """Retrieve the paymentAuthorizationToken using the client_id|client_secret pair
        or collect it from the cache if an unexpired paymentAuthorizationToken exist.
        """
        cache_key = f"payment|{self.settings.carrier_name}|{self.settings.client_id}|{self.settings.client_secret}"

        def get_token():
            # First ensure we have a valid access token
            access_token = self.authenticate().deserialize()

            result = lib.request(
                url=f"{self.settings.server_url}/payments/v3/payment-authorization",
                trace=self.settings.trace_as("json"),
                method="POST",
                headers={
                    "content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
                data=lib.to_json(
                    {
                        "roles": [
                            {
                                "roleName": "LABEL_OWNER",
                                "CRID": self.settings.CRID,
                                "MID": self.settings.MID,
                                "accountType": self.settings.account_type or "EPS",
                                "accountNumber": self.settings.account_number,
                                "manifestMID": self.settings.manifest_MID,
                            },
                            {
                                "roleName": "PAYER",
                                "CRID": self.settings.CRID,
                                "MID": self.settings.MID,
                                "accountType": self.settings.account_type or "EPS",
                                "accountNumber": self.settings.account_number,
                            },
                        ]
                    }
                ),
                max_retries=2,
            )

            response = lib.to_dict(result)
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages)

            expiry = datetime.datetime.now() + datetime.timedelta(minutes=50)

            return {**response, "expiry": lib.fdatetime(expiry)}

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="paymentAuthorizationToken",
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.run_asynchronously(
            lambda _: lib.request(
                url=f"{self.settings.server_url}/shipments/v3/options/search",
                data=lib.to_json(_),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            ),
            request.serialize(),
        )

        return lib.Deserializable(response, lambda _: [lib.to_dict(_) for _ in _])

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        payment_token = self.get_payment_token().deserialize()
        response = lib.run_asynchronously(
            lambda _: lib.request(
                url=f"{self.settings.server_url}/international-labels/v3/international-label",
                data=lib.to_json(_),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                    "X-Payment-Authorization-Token": f"{payment_token}",
                },
                on_error=provider_utils.parse_error_response,
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda _: [provider_utils.parse_response(_) for _ in _],
            request.ctx,
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        payment_token = self.get_payment_token().deserialize()
        response = lib.run_asynchronously(
            lambda _: (
                _["trackingNumber"],
                lib.request(
                    url=f"{self.settings.server_url}/international-labels/v3/international-label/{_['trackingNumber']}",
                    trace=self.trace_as("json"),
                    method="DELETE",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {access_token}",
                        "X-Payment-Authorization-Token": f"{payment_token}",
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [(_[0], lib.to_dict(_[1])) for _ in __],
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.run_asynchronously(
            lambda trackingNumber: (
                trackingNumber,
                lib.request(
                    url=f"{self.settings.server_url}/tracking/v3/tracking/{trackingNumber}?expand=DETAIL",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {access_token}",
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            response,
            lambda __: [(_[0], lib.to_dict(_[1])) for _ in __],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v3/carrier-pickup",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v3/carrier-pickup/{request.ctx['confirmationNumber']}",
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
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/pickup/v3/carrier-pickup/{request.serialize()['confirmationNumber']}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            on_ok=lambda _: '{"ok": true}',
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/scan-forms/v3/scan-form",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
