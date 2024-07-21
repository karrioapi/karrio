"""Karrio HayPost client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.hay_post.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/Api/Order/CalculateTariff",
            data=lib.to_json(lib.to_list(request.serialize())),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": self.settings.authorization,
            },
            proxy=self.settings.proxy,
        )

        response_dict = {"rates": response, "request": request.value}

        return lib.Deserializable(response_dict, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/Api/Order/CreateOrderByCustomerShort",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": self.settings.authorization,
            },
            proxy=self.settings.proxy,
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        query = request.serialize()
        trackingnumber = query[0]

        response = lib.request(
            url=f"{self.settings.server_url}/Api/Order/Tracking/{trackingnumber}",
            trace=self.trace_as("json"),
            method="GET",
            proxy=self.settings.proxy,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": self.settings.authorization,
            },
        )

        return lib.Deserializable(response, lib.to_dict)
