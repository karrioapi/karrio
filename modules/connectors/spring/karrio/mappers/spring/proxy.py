"""Karrio Spring client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.spring.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create shipments using Spring OrderShipment API.

        Spring is a per-package carrier, so we make parallel requests
        for each package and return a list of responses.
        """
        responses = lib.run_asynchronously(
            lambda req: lib.request(
                url=self.settings.server_url,
                data=lib.to_json(req),
                trace=self.trace_as("json"),
                method="POST",
                headers={"Content-Type": "text/json"},
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [lib.to_dict(res) for res in __],
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={"Content-Type": "text/json"},
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Track shipments using Spring TrackShipment API.

        Spring tracks one shipment at a time, so we make parallel requests
        for each tracking number and return results as (tracking_number, response) tuples.
        """
        responses = lib.run_asynchronously(
            lambda req: (
                req["Shipment"]["TrackingNumber"],
                lib.request(
                    url=self.settings.server_url,
                    data=lib.to_json(req),
                    trace=self.trace_as("json"),
                    method="POST",
                    headers={"Content-Type": "text/json"},
                ),
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda __: [(tracking_number, lib.to_dict(res)) for tracking_number, res in __],
        )
