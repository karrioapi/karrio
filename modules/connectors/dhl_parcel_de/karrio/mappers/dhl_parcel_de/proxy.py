"""Karrio DHL Parcel DE client proxy."""

import typing
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dhl_parcel_de.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = urllib.parse.urlencode(request.ctx)
        response = lib.request(
            url=f"{self.settings.server_url}/v2/orders?{query}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-type": "application/json",
                "dhl-api-key": self.settings.dhl_api_key,
                "Accept-Language": self.settings.language,
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = lib.request(
            url=f"{self.settings.server_url}/v2/orders?{query}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "content-type": "application/json",
                "DHL-API-Key": self.settings.dhl_api_key,
                "Accept-Language": self.settings.language,
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:

        if not all([self.settings.tracking_consumer_key]):
            raise Exception(
                "The tracking_consumer_key is required for Track API requests."
            )

        responses: typing.List[dict] = lib.run_asynchronously(
            lambda request: lib.request(
                url=f"{self.settings.tracking_server_url}/track/shipments?{urllib.parse.urlencode(request)}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "DHL-API-Key": self.settings.tracking_consumer_key,
                },
            ),
            request.serialize(),
        )

        return lib.Deserializable(responses, lambda res: [lib.to_dict(r) for r in res])
