"""Karrio GLS client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.gls_eu.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/backend/rs/shipments",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/backend/rs/shipments/cancel/{request.serialize()}",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _get_tracking(trackId: str):
            return trackId, lib.request(
                url=f"{self.settings.server_url}/backend/rs/tracking/parcels",
                data=dict(TrackID=trackId),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
            )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_concurently(
            _get_tracking, request.serialize()
        )

        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )
