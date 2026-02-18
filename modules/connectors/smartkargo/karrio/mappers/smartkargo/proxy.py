"""Karrio SmartKargo client proxy."""

import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.smartkargo.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/quotation",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "code": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # Step 1: Create the booking
        response = lib.request(
            url=f"{self.settings.server_url}/exchange/single?version=2.0",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "code": self.settings.api_key,
            },
        )

        raw_response = lib.to_dict(response)
        # API returns array-wrapped response like [{...}], unwrap it
        shipment_response = raw_response[0] if isinstance(raw_response, list) else raw_response

        # Step 2: Fetch labels for all shipments (conditionally, like Sendle's abort pattern)
        shipments = shipment_response.get("shipments") or []
        label_type = request.ctx.get("label_type", "PDF") if request.ctx else "PDF"
        format_param = "&format=zpl" if label_type.upper() == "ZPL" else ""

        labels = lib.run_asynchronously(
            lambda shipment: (
                lib.to_dict(
                    lib.request(
                        url=f"{shipment['labelUrl']}{format_param}",
                        trace=self.trace_as("json"),
                        method="GET",
                        headers={
                            "Content-Type": "application/json",
                            "code": self.settings.api_key,
                        },
                    )
                )
                if shipment.get("labelUrl") and shipment.get("status") == "Booked"
                else {}
            ),
            shipments,
        )

        return lib.Deserializable(
            (shipment_response, labels),
            lambda data: data,
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
        """Cancel/void a shipment that hasn't departed yet."""
        payload = request.serialize()

        # Build query parameters with proper URL encoding
        params = {
            k: v for k, v in {
                "prefix": payload["prefix"],
                "airWaybill": payload["airWaybill"],
                "userName": payload.get("userName"),
                "reason": payload.get("reason"),
            }.items() if v is not None
        }

        response = lib.request(
            url=f"{self.settings.server_url}/shipment/void?{urllib.parse.urlencode(params)}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "code": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

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
