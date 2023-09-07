"""Karrio Asendia US client proxy."""

import typing
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.asendia_us.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/A1/v1.0/ShippingPlatform/ShippingRate?{request.serialize()}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/A1/v1.0/ShippingPlatform/Package",
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
            url=f"{self.settings.server_url}/api/A1/v1.0/ShippingPlatform/Package?{request.serialize()}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/api/A1/v2.0/Tracking/Detail?trackingNumberVendor={tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
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
