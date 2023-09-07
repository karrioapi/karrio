"""Karrio Deutsche Post International client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dpdhl_international.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v1/orders",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _get_tracking(awb: str):
            return lib.request(
                url=f"{self.settings.server_url}/dpi/tracking/v3/trackings/awb/{awb}",
                data=request.serialize(),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "accept": "application/json",
                    "content-type": "application/json",
                    "Authorization": f"Bearer {self.settings.access_token}",
                },
            )

        responses: typing.List[dict] = lib.run_asynchronously(
            _get_tracking, request.serialize()
        )

        return lib.Deserializable(responses, lambda res: [lib.to_dict(r) for r in res])
