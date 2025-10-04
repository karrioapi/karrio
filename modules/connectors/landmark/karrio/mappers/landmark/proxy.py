"""Karrio Landmark Global client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.universal.mappers.rating_proxy as rating_proxy
import karrio.mappers.landmark.settings as provider_settings


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/{request.ctx['API']}.php",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "application/xml",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/Cancel.php",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "application/xml",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable[str]:
        responses = lib.run_concurently(
            lambda request: (
                request.number,
                lib.request(
                    url=f"{self.settings.server_url}/Track.php",
                    data=request.request,
                    trace=self.trace_as("xml"),
                    method="POST",
                    headers={
                        "Content-Type": "application/xml",
                    },
                ),
            ),
            requests.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_element(track)) for num, track in res if any(track.strip())
            ],
        )
