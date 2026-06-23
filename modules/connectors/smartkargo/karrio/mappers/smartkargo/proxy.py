"""Karrio SmartKargo client proxy."""

import urllib.parse

import karrio.api.proxy as proxy
import karrio.lib as lib
import karrio.mappers.smartkargo.settings as provider_settings
import karrio.providers.smartkargo.utils as provider_utils


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        site_id = self.settings.connection_config.site_id.state
        _trace = self.trace_as("json")
        responses = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/quotation",
                data=lib.to_json(payload),
                trace=_trace,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "code": self.settings.api_key,
                    **({"SiteId": site_id} if site_id else {}),
                },
                on_error=provider_utils.parse_http_error,
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [lib.to_dict(_) for _ in __],
        )

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        label_type = request.ctx.get("label_type", "PDF") if request.ctx else "PDF"
        format_param = "&format=zpl" if label_type.upper() == "ZPL" else ""
        site_id = self.settings.connection_config.site_id.state
        _trace = self.trace_as("json")

        # Step 1: Book each package in parallel (one API call per package)
        booking_responses = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/exchange/single?version=2.0",
                data=lib.to_json(payload),
                trace=_trace,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "code": self.settings.api_key,
                    **({"SiteId": site_id} if site_id else {}),
                },
                on_error=provider_utils.parse_http_error,
            ),
            request.serialize(),
        )

        # Step 2: Fetch label for each booking response in parallel
        responses = lib.run_asynchronously(
            lambda data: (
                data["response"],
                (
                    lib.to_dict(
                        lib.request(
                            url=f"{data['label_url']}{format_param}",
                            trace=_trace,
                            method="GET",
                            headers={
                                "Content-Type": "application/json",
                                "code": self.settings.api_key,
                                **({"SiteId": site_id} if site_id else {}),
                            },
                            on_error=provider_utils.parse_http_error,
                        )
                    )
                    if data.get("label_url")
                    else {}
                ),
            ),
            [provider_utils.extract_booking_data(raw) for raw in booking_responses],
        )

        return lib.Deserializable(
            responses,
            lambda __: [(response, label) for response, label in __],
            ctx=request.ctx,
        )

    def get_label(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Fetch label for a shipment using labelUrl from shipment meta."""
        payload = request.serialize()
        label_url = payload["labelUrl"]
        label_type = payload.get("labelType", "PDF")
        format_param = "&format=zpl" if label_type.upper() == "ZPL" else ""
        site_id = self.settings.connection_config.site_id.state

        response = lib.request(
            url=f"{label_url}{format_param}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "code": self.settings.api_key,
                **({"SiteId": site_id} if site_id else {}),
            },
            on_error=provider_utils.parse_http_error,
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel/void shipment(s). For multi-piece, cancels each package in parallel."""
        site_id = self.settings.connection_config.site_id.state
        _trace = self.trace_as("json")
        responses = lib.run_asynchronously(
            lambda payload: (
                f"{payload.get('prefix', '')}{payload.get('airWaybill', '')}",
                lib.request(
                    url=(
                        f"{self.settings.server_url}/shipment/void?"
                        f"{urllib.parse.urlencode({k: v for k, v in payload.items() if v is not None})}"
                    ),
                    trace=_trace,
                    method="GET",
                    headers={
                        "Content-Type": "application/json",
                        "code": self.settings.api_key,
                        **({"SiteId": site_id} if site_id else {}),
                    },
                    on_error=provider_utils.parse_http_error,
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [(tracking_number, provider_utils.parse_void_response(raw)) for tracking_number, raw in __],
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        tracking_requests = request.serialize()
        _trace = self.trace_as("json")

        # Resolve tracking endpoint: partner URL takes precedence when configured
        _partner_url = self.settings.connection_config.partner_tracking_url.state
        _base_url = f"{_partner_url}/api" if _partner_url else self.settings.server_url
        _code = (
            self.settings.connection_config.partner_tracking_api_code.state
            if _partner_url
            else self.settings.api_key
        ) or self.settings.api_key
        _site_id = self.settings.connection_config.site_id.state

        responses = lib.run_asynchronously(
            lambda payload: (
                payload["tracking_number"],
                lib.request(
                    url=f"{_base_url}/tracking?{urllib.parse.urlencode(payload['query_params'])}",
                    trace=_trace,
                    method="GET",
                    headers={
                        "Content-Type": "application/json",
                        "code": _code,
                        **({"SiteId": _site_id} if _site_id else {}),
                    },
                    on_error=provider_utils.parse_http_error,
                ),
            ),
            tracking_requests,
        )

        return lib.Deserializable(
            responses,
            lambda __: [(ref, lib.to_dict(_)) for ref, _ in __],
        )
