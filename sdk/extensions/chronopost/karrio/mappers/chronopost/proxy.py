import typing
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
from karrio.core.utils import (
    Envelope,
    XP,
    request as http,
    exec_parrallel,
)
import karrio.mappers.chronopost.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def _send_request(self, request: lib.Serializable, path: str) -> str:
        return lib.request(
            url=f"{self.settings.server_url}{path}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
            },
            method="POST",
        )

    def get_rates(
        self,
        request: lib.Serializable,
    ) -> lib.Deserializable:
        response = self._send_request(request, path="/quickcost-cxf/QuickcostServiceWS")
        return lib.Deserializable(response, lib.to_element)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request(request, path="/shipping-cxf/ShippingServiceWS")

        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self._send_request(request, path="/tracking-cxf/TrackingServiceWS")

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(
        self, request: lib.Serializable[typing.List[str]]
    ) -> lib.Deserializable[str]:
        response = self._send_request(request, path="/tracking-cxf/TrackingServiceWS")

        return lib.Deserializable(response, lib.to_element)
