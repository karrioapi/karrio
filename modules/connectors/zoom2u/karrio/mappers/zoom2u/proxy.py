"""Karrio Zoom2u client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.zoom2u.error as provider_error
import karrio.providers.zoom2u.utils as provider_utils
import karrio.mappers.zoom2u.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/v1/delivery/quote",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
            on_error=provider_error.parse_http_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/v1/delivery/create",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
            on_error=provider_error.parse_http_response,
        )

        return lib.Deserializable(
            response,
            lambda _: lib.to_dict(provider_utils.clean_response(_)),
        )

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/api/v1/delivery/cancel/{payload['reference']}",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
            on_error=provider_error.parse_http_response,
            decoder=lambda _: dict(ok=True),
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _get_tracking(reference: str):
            return reference, lib.request(
                url=f"{self.settings.server_url}/api/v1/delivery/status/{reference}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.settings.api_key}",
                },
                on_error=provider_error.parse_http_response,
            )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_concurently(
            _get_tracking, request.serialize()
        )

        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(provider_utils.clean_response(track)))
                for num, track in res
                if any(track.strip())
            ],
        )
