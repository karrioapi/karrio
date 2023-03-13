"""Karrio DPD client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dpd.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={},
        )

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable[str]:
        def _track(payload):
            tracking_number, data = payload
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}",
                trace=self.trace_as("xml"),
                method="POST",
                data=data,
            )

        responses = lib.run_concurently(_track, requests.serialize().items())

        return lib.Deserializable(
            responses,
            lambda results: [(res[0], lib.to_element(res[1])) for res in results],
        )
