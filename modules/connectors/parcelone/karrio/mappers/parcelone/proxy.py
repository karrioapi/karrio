"""Karrio ParcelOne client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.parcelone.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://tempuri.org/IShippingWCF/getCharges",
            },
        )

        return lib.Deserializable(response, lib.to_element, request.ctx)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://tempuri.org/IShippingWCF/registerShipments",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://tempuri.org/IShippingWCF/voidShipments",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://tempuri.org/IShippingWCF/getTrackings",
            },
        )

        return lib.Deserializable(response, lib.to_element)
