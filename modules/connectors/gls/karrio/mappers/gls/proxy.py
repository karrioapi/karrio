"""Karrio GLS Group client proxy."""

import karrio.api.proxy as proxy
import karrio.lib as lib
import karrio.mappers.gls.settings as provider_settings
import karrio.providers.gls.utils as provider_utils
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
                "Content-Type": "application/glsVersion1+json",
                "Accept": "application/glsVersion1+json",
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
                "Content-Type": "application/glsVersion1+json",
                "Accept": "application/glsVersion1+json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_locations(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Look up GLS ParcelShops. URL/method/body are resolved by
        ``location_request`` and packed into ``request.ctx``."""
        ctx = request.ctx or {}
        response = lib.request(
            url=ctx["url"],
            method=ctx.get("method", "GET"),
            data=lib.to_json(request.serialize()) if ctx.get("has_body") else None,
            trace=self.trace_as("json"),
            headers={
                "Content-Type": "application/glsVersion1+json",
                "Accept": "application/glsVersion1+json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Track parcels using the GLS Track and Trace API."""
        tracking_numbers = request.serialize()
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
                "Content-Type": "application/glsVersion1+json",
                "Accept": "application/glsVersion1+json",
                "Authorization": f"Bearer {self.settings.access_token}",
            },
            on_error=provider_utils.parse_error_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_return_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        return self.create_shipment(request)

    def upload_document(self, request: lib.Serializable) -> lib.Deserializable:
        """GLS paperless post_upload chain — see SPECS.md › Paperless trade document upload."""
        envelopes = request.serialize()
        ctx = request.ctx or {}
        files = ctx.get("files") or []
        responses: list[dict] = [
            provider_utils.upload_one_document(self.settings, envelope, document)
            for envelope, document in zip(envelopes, files, strict=False)
        ]

        customs_response = provider_utils.post_customs_consignment(self.settings, responses, ctx)
        if customs_response is not None:
            responses = [*responses, customs_response]

        return lib.Deserializable(responses, lambda r: r)
