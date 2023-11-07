from karrio.core.utils import request as http, XP
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.freightcom.settings import Settings
from karrio.core.utils.serializable import Serializable, Deserializable


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable) -> Deserializable:
        response = http(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={"Content-Type": "application/xml"},
        )
        return Deserializable(response, XP.to_xml)

    def create_shipment(self, request: Serializable) -> Deserializable:
        response = http(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={"Content-Type": "application/xml"},
        )
        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable) -> Deserializable:
        response = http(
            url=self.settings.server_url,
            data=request.serialize(),
            trace=self.trace_as("xml"),
            method="POST",
            headers={"Content-Type": "application/xml"},
        )
        return Deserializable(response, XP.to_xml)
