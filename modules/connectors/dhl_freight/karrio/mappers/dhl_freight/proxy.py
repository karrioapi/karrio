"""Karrio DHL Freight client proxy."""

import base64
import datetime
import urllib.parse

import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.lib as lib
import karrio.mappers.dhl_freight.settings as provider_settings
import karrio.providers.dhl_freight.error as provider_error
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, request: lib.Serializable = None) -> lib.Deserializable[str]:
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exists.

        DHL Freight uses the shared DHL Authentication API (client_credentials)
        with Basic Auth header, query-string grant params, and an empty (but
        length-bearing) POST body. See SPECS.md "Authentication".
        """
        basic_auth = base64.b64encode(
            f"{self.settings.connection_client_id}:{self.settings.connection_client_secret}".encode()
        ).decode()

        def get_token():
            response = lib.request(
                url=f"{self.settings.token_server_url}?grant_type=client_credentials&response_type=access_token",
                trace=self.settings.trace_as("json"),
                data="",  # empty body → Content-Length: 0; marks request as POST
                method="POST",
                headers={
                    "Authorization": f"Basic {basic_auth}",
                    "Accept": "application/json",
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

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=f"{self.settings.carrier_name}|{self.settings.connection_client_id}|{self.settings.connection_client_secret}",
            buffer_minutes=5,
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # Rate-sheet only (services.csv); no live Rates API. See SPECS.md.
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        ctx = lib.to_dict(request.ctx) or {}
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/sendtransportinstruction",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Accept": "application/json",
                "Accept-Language": self.settings.language,
                "Authorization": f"Bearer {access_token}",
            },
        )

        # Print (Labelling) API follow-up (PRD §6.3) — opt-in & fail-open: only
        # runs when `auto_print_documents` is enabled and the booking returned a
        # shipment id; any print failure is swallowed so the booking still
        # succeeds (label simply stays empty). Returns (booking, print|None).
        print_doc = None
        booking = lib.to_dict(response)
        shipment_id = booking.get("shipmentId") or booking.get("transportInstructionId")
        if ctx.get("auto_print") and shipment_id:
            print_doc = lib.failsafe(
                lambda: lib.request(
                    url=f"{self.settings.print_server_url}/print/printdocumentsbyid",
                    data=lib.to_json(
                        dict(
                            shipmentId=[str(shipment_id)],
                            printOption=ctx.get("print_document_type") or "label",
                        )
                    ),
                    trace=self.trace_as("json"),
                    method="POST",
                    headers={
                        "content-type": "application/json",
                        "Accept": "application/json",
                        "Authorization": f"Bearer {access_token}",
                    },
                )
            )

        return lib.Deserializable(
            (response, print_doc),
            lambda pair: (lib.to_dict(pair[0]), lib.to_dict(pair[1]) if pair[1] else None),
            ctx,
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # UTAPI uses a DHL-API-Key header (the client_id), not the OAuth token.
        # One GET per tracking number, run concurrently.
        responses = lib.run_asynchronously(
            lambda query: lib.request(
                url=f"{self.settings.tracking_server_url}/shipments?{urllib.parse.urlencode(query)}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "DHL-API-Key": self.settings.connection_client_id,
                },
                on_error=lib.error_decoder,
            ),
            request.serialize(),
        )

        return lib.Deserializable(responses, lambda res: [lib.to_dict(r) for r in res])
