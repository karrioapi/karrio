import karrio.lib as lib
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.dhl_express.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    def _send_request(self, request: lib.Serializable) -> str:
        return lib.request(
            url=f"{self.settings.server_url}/XMLShippingServlet",
            data=request.serialize(),
            headers={"Content-Type": "application/xml"},
            trace=self.trace_as("xml"),
            method="POST",
        )

    def validate_address(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request)

        return lib.Deserializable(response, lib.to_element)

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request)

        return lib.Deserializable(response, lib.to_element, request.ctx)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request)

        return lib.Deserializable(response, lib.to_element)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request)

        return lib.Deserializable(response, lib.to_element)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request)

        return lib.Deserializable(response, lib.to_element)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request)

        return lib.Deserializable(response, lib.to_element)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(request)

        return lib.Deserializable(response, lib.to_element)

    def upload_document(self, request: lib.Serializable) -> lib.Deserializable:
        return super().upload_document(request)
