"""Karrio TGE client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.tge.utils as provider_utils
import karrio.mappers.tge.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/calculatePrice",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Auth": f"Basic {self.settings.auth}",
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, provider_utils.parse_response, request.ctx)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/printlabel",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "x-mytoll-identity": self.settings.my_toll_identity,
                "x-mytoll-token": self.settings.my_toll_token,
                "x-api-key": self.settings.api_key,
                "Content-Type": "application/json",
                "accept": "*/*",
            },
        )

        return lib.Deserializable(response, provider_utils.parse_response, request.ctx)
