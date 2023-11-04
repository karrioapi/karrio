"""Karrio DHL Poland client proxy module."""
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.universal.mappers.rating_proxy as rating_proxy
import karrio.mappers.dhl_poland.settings as provider_settings


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def _send_request(self, request: lib.Serializable, soapaction: str) -> str:
        return lib.request(
            url=f"{self.settings.server_url}",
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "soapaction": soapaction,
            },
        )

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        responses = lib.run_asynchronously(
            lambda request: dict(
                number=request[0],
                data=self._send_request(
                    lib.Serializable(request[1]),
                    soapaction=f"{self.settings.server_url}#getTrackAndTraceInfo",
                ),
            ),
            requests.serialize().items(),
        )

        return lib.Deserializable(
            responses,
            lambda results: {
                result["number"]: lib.to_element(result["data"]) for result in results
            },
        )

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            request,
            soapaction=f"{self.settings.server_url}#createShipment",
        )

        return lib.Deserializable(response, lib.to_element)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            request,
            soapaction=f"{self.settings.server_url}#deleteShipment",
        )

        return lib.Deserializable(response, lib.to_element)
