"""Karrio Post NL client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.postnl.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/shipment/v1/checkout",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/shipment/v2_2/label",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable[str]:
        language = self.settings.connection_config.language.state or "EN"

        track = lambda barcode: (
            barcode,
            lib.request(
                url=f"{self.settings.server_url}/shipment/v2/status/barcode/{barcode}?language={language}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    "apikey": self.settings.api_key,
                },
            ),
        )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            track, requests.serialize()
        )

        return lib.Deserializable(
            responses,
            lambda response: [(key, lib.to_dict(res)) for key, res in response],
        )
