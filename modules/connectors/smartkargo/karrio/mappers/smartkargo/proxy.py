"""Karrio SmartKargo client proxy."""

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
        # Step 1: Create the shipment/exchange
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

        shipment_response = lib.to_dict(response)

        # Step 2: Fetch labels asynchronously for each booked shipment
        shipments = shipment_response.get("shipments") or []
        label_type = request.ctx.get("label_type", "PDF") if request.ctx else "PDF"

        # Build label fetch requests with index to maintain order
        # API manual: format=zpl for ZPL, omit parameter for PDF (default)
        format_param = "&format=zpl" if label_type.upper() == "ZPL" else ""
        label_requests = [
            dict(
                index=idx,
                prefix=shipment.get("prefix"),
                air_waybill=shipment.get("airWaybill"),
            )
            for idx, shipment in enumerate(shipments)
            if shipment.get("prefix")
            and shipment.get("airWaybill")
            and shipment.get("status") == "Booked"
        ]

        # Initialize labels list with empty dicts for all shipments
        labels = [{} for _ in shipments]

        # Fetch labels asynchronously for better performance
        if label_requests:
            label_responses = lib.run_asynchronously(
                lambda payload: (
                    payload["index"],
                    lib.request(
                        url=f"{self.settings.server_url}/label?prefix={payload['prefix']}&airWaybill={payload['air_waybill']}{format_param}",
                        trace=self.trace_as("json"),
                        method="GET",
                        headers={
                            "Content-Type": "application/json",
                            "code": self.settings.api_key,
                        },
                    ),
                ),
                label_requests,
            )
            # Place labels at correct indices
            for idx, resp in label_responses:
                labels[idx] = lib.to_dict(resp)

        # Combine shipment response with labels and pass context
        return lib.Deserializable(
            (shipment_response, labels),
            lambda data: data,
            ctx=request.ctx,
        )

    def get_label(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Fetch label for a shipment using prefix and airWaybill."""
        payload = request.serialize()
        # API manual: format=zpl for ZPL, omit parameter for PDF (default)
        label_type = payload.get('labelType', 'PDF')
        format_param = "&format=zpl" if label_type.upper() == "ZPL" else ""
        response = lib.request(
            url=f"{self.settings.server_url}/label?prefix={payload['prefix']}&airWaybill={payload['airWaybill']}{format_param}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "code": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel a shipment."""
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/void?prefix={payload['prefix']}&airWaybill={payload['airWaybill']}",
            trace=self.trace_as("json"),
            method="DELETE",
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
