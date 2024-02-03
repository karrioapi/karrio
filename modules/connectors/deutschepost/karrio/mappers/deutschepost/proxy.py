"""Karrio Deutsche Post Germany client proxy."""

import typing
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.deutschepost.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v2/orders",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v2/orders?profile=STANDARD_GRUPPENPROFIL&shipment={request.serialize()}",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _get_tracking(tracking_request: dict):
            query = urllib.parse.urlencode(tracking_request)
            return lib.request(
                url=f"{self.settings.tracking_server_url}/track/shipments?{query}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "DHL-API-Key": self.settings.tracking_consumer_key,
                },
            )

        responses: typing.List[dict] = lib.run_asynchronously(
            _get_tracking, request.serialize()
        )

        return lib.Deserializable(responses, lambda res: [lib.to_dict(r) for r in res])
