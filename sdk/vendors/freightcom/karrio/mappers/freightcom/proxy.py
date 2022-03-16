from karrio.core.utils import request as http, XP
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.freightcom.settings import Settings
from karrio.core.utils.serializable import Serializable, Deserializable


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, XP.to_xml)

    def create_shipment(self, request: Serializable) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, XP.to_xml)

    def cancel_shipment(self, request: Serializable) -> Deserializable[str]:
        response = http(
            url=self.settings.server_url,
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, XP.to_xml)
