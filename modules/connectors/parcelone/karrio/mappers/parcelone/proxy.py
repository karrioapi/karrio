"""Karrio ParcelOne REST API client proxy."""

import karrio.api.proxy as proxy
import karrio.lib as lib
import karrio.mappers.parcelone.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[list]:
        """Create one vendor shipment per parcel in parallel (Pattern B fan-out)."""
        responses = lib.run_asynchronously(
            lambda payload: lib.request(
                url=f"{self.settings.server_url}/shippingapi/v1/shipment",
                data=lib.to_json(payload),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": self.settings.authorization,
                    "Apikey": self.settings.api_key,
                },
            ),
            request.serialize(),
        )

        return lib.Deserializable(
            responses,
            lambda items: [lib.to_dict(r) for r in items],
            request.ctx,
        )

    def create_return_shipment(self, request: lib.Serializable) -> lib.Deserializable[list]:
        return self.create_shipment(request)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[dict]:
        """Cancel a shipment via DELETE /shipment/{ref_field}/{ref_value}."""
        data = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/shippingapi/v1/shipment/{data['ref_field']}/{data['ref_value']}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Accept": "application/json",
                "Authorization": self.settings.authorization,
                "Apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_profile(self) -> lib.Deserializable[dict]:
        """Fetch the mandator profile (per-customer CEP / Product / Service portfolio)."""
        response = lib.request(
            url=f"{self.settings.server_url}/shippingapi/v1/profile",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": "application/json",
                "Authorization": self.settings.authorization,
                "Apikey": self.settings.api_key,
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[list]:
        """Fetch TrackLMC events for each tracking number.

        GET {tracklmc_url}/shipment/{trackno} per the TrackLMC OpenAPI spec.
        """
        responses = [
            (
                req["tracking_number"],
                lib.to_dict(
                    lib.request(
                        url=f"{self.settings.server_url}/tracklmc/shipment/{req['tracking_number']}",
                        trace=self.trace_as("json"),
                        method="GET",
                        headers={
                            "Accept": "application/json",
                            "Authorization": self.settings.authorization,
                            "Apikey": self.settings.api_key,
                        },
                    )
                ),
            )
            for req in request.serialize()
        ]

        return lib.Deserializable(responses, lambda x: x)
