"""Karrio SmartKargo client proxy."""

import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.smartkargo.utils as provider_utils
import karrio.mappers.smartkargo.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        responses = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/quotation",
                data=lib.to_json(payload),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "code": self.settings.api_key,
                },
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

        # Step 1: Book each package in parallel (one API call per package)
        booking_responses = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/exchange/single?version=2.0",
                data=lib.to_json(payload),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "code": self.settings.api_key,
                },
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
                            trace=self.trace_as("json"),
                            method="GET",
                            headers={
                                "Content-Type": "application/json",
                                "code": self.settings.api_key,
                            },
                        )
                    )
                    if data.get("label_url")
                    else {}
                ),
            ),
            [
                provider_utils.extract_booking_data(raw)
                for raw in booking_responses
            ],
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

        response = lib.request(
            url=f"{label_url}{format_param}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "code": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel/void shipment(s). For multi-piece, cancels each package in parallel."""
        responses = lib.run_asynchronously(
            lambda payload: (
                f"{payload.get('prefix', '')}{payload.get('airWaybill', '')}",
                lib.request(
                    url=(
                        f"{self.settings.server_url}/shipment/void?"
                        f"{urllib.parse.urlencode({k: v for k, v in payload.items() if v is not None})}"
                    ),
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "Content-Type": "application/json",
                        "code": self.settings.api_key,
                    },
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [
                (tracking_number, provider_utils.parse_void_response(raw))
                for tracking_number, raw in __
            ],
        )

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        tracking_requests = request.serialize()

        responses = lib.run_asynchronously(
            lambda payload: (
                payload["tracking_number"],
                lib.request(
                    url=f"{self.settings.server_url}/tracking?packageReference={payload['tracking_number']}",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "Content-Type": "application/json",
                        "code": self.settings.api_key,
                    },
                ),
            ),
            tracking_requests,
        )

        return lib.Deserializable(
            responses,
            lambda __: [(ref, lib.to_dict(_)) for ref, _ in __],
        )
