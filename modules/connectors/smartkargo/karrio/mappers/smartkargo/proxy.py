"""Karrio SmartKargo client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.smartkargo.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/quotation?version=2.0",
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

        return lib.Deserializable(response, lib.to_dict)

    def get_label(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Fetch label for a shipment using prefix and airWaybill."""
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/label?prefix={payload['prefix']}&airWaybill={payload['airWaybill']}&labelType={payload.get('labelType', 'PDF')}",
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
