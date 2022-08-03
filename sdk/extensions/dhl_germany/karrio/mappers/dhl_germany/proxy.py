
"""Karrio DHL Parcel Germany client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.mappers.dhl_germany.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers=None,
        )

        return lib.Deserializable(response, lib.to_element)
    
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers=None,
        )

        return lib.Deserializable(response, lib.to_element)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers=None,
        )

        return lib.Deserializable(response, lib.to_element)
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers=None,
        )

        return lib.Deserializable(response, lib.to_element)
    