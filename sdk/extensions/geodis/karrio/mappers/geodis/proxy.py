"""Karrio GEODIS client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.geodis.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        service = "api/zoomclient/recherche-envoi"
        track = lambda data: (
            data["noSuivi"],
            lib.request(
                url=f"{self.settings.server_url}/{service}",
                trace=self.trace_as("json"),
                method="POST",
                data=data,
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
