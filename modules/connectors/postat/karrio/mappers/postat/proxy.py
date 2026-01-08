"""Karrio PostAT client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.postat.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a shipment using ImportShipment SOAP operation."""
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://post.ondot.at/IShippingService/ImportShipment",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel a shipment using CancelShipments SOAP operation."""
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://post.ondot.at/IShippingService/CancelShipments",
            },
        )

        return lib.Deserializable(response, lib.to_element)
