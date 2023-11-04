"""Karrio Asendia US client proxy."""

import typing
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.asendia_us.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = lib.request(
            url=f"{self.settings.server_url}/api/A1/v1.0/ShippingPlatform/ShippingRate?{query}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": "application/json",
                "X-AsendiaOne-ApiKey": f"{self.settings.api_key}",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/A1/v1.0/ShippingPlatform/Package",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "X-AsendiaOne-ApiKey": f"{self.settings.api_key}",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = lib.request(
            url=f"{self.settings.server_url}/api/A1/v1.0/ShippingPlatform/Package?{query}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Accept": "application/json",
                "X-AsendiaOne-ApiKey": f"{self.settings.api_key}",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        trackingNumberVendor = ",".join(request.serialize())
        response = lib.request(
            url=f"{self.settings.server_url}/api/A1/v2.0/Tracking/Milestone?trackingNumberVendor={trackingNumberVendor}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Accept": "application/json",
                "X-AsendiaOne-ApiKey": f"{self.settings.api_key}",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
