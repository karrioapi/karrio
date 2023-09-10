"""Karrio Locate2u client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.locate2u.error as provider_error
import karrio.mappers.locate2u.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/v1/stops",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_error.parse_http_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/api/v1/stops/{payload['stopId']}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_error.parse_http_response,
            decoder=lambda _: dict(ok=True),
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _get_tracking(stop_id: str):
            return stop_id, lib.request(
                url=f"{self.settings.server_url}/api/v1/stops/{stop_id}?includeItems=false&includeLines=false",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.settings.access_token}",
                },
                on_error=provider_error.parse_http_response,
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
