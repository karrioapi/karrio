"""Karrio Veho client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.veho.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v2/quote/rate",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v2/orders",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        order_id = request.serialize().get("order_id")
        
        response = lib.request(
            url=f"{self.settings.server_url}/v2/orders/{order_id}/events/cancelled",
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "Content-Type": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        responses = lib.run_asynchronously(
            lambda data: (
                data["tracking_number"],
                lib.request(
                    url=f"{self.settings.server_url}/v2/packages/{data['tracking_number']}",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "Content-Type": "application/json",
                        "apikey": self.settings.api_key,
                    },
                ),
            ),
            [_ for _ in request.serialize() if _.get("tracking_number")],
        )

        return lib.Deserializable(
            responses,
            lambda __: [(_[0], lib.to_dict(_[1])) for _ in __],
        ) 
