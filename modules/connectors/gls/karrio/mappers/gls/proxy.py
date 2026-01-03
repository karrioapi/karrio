"""Karrio GLS Group client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.gls.utils as provider_utils
import karrio.mappers.gls.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.shipment_api_url}/rs/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel a shipment by track ID."""
        track_id = request.serialize()
        response = lib.request(
            url=f"{self.settings.shipment_api_url}/rs/shipments/cancel/{track_id}",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Track parcels using the GLS Track and Trace API."""
        tracking_numbers = request.serialize()

        # The GLS T&T API accepts up to 10 tracking numbers in a single request
        # Join them with commas for batch tracking
        tracking_ids = ",".join(tracking_numbers)

        response = lib.request(
            url=f"{self.settings.tracking_api_url}/tracking/simple/trackids/{tracking_ids}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(
            response,
            lambda res: lib.to_dict(res),
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Schedule a sporadic collection (pickup) with GLS."""
        response = lib.request(
            url=f"{self.settings.shipment_api_url}/rs/sporadiccollection",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)
