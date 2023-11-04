"""Karrio GEODIS client proxy."""

import json
import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.geodis.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        service = "api/wsclient/enregistrement-envois"
        data = request.serialize()

        response = lib.request(
            url=f"{self.settings.server_url}/{service}",
            data=json.dumps(data, separators=(",", ":")),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "*/*",
                "Content-Type": "application/json",
                "X-GEODIS-Service": self.settings.get_token(service, data),
            },
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        service = "api/wsclient/suppression-envois"
        data = request.serialize()

        response = lib.request(
            url=f"{self.settings.server_url}/{service}",
            data=json.dumps(data, separators=(",", ":")),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "*/*",
                "Content-Type": "application/json",
                "X-GEODIS-Service": self.settings.get_token(service, data),
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        service = "api/zoomclient/recherche-envoi"
        track = lambda data: (
            data["noSuivi"],
            lib.request(
                url=f"{self.settings.server_url}/{service}",
                trace=self.trace_as("json"),
                method="POST",
                data=json.dumps(data, separators=(",", ":")),
                headers={
                    "Content-Type": "application/json",
                    "X-GEODIS-Service": self.settings.get_token(service, data),
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
