from purplship.core.utils import to_xml, request as http, Element
from purplship.package.proxy import Proxy as BaseProxy
from purplship.extension.mappers.freightcom.settings import Settings
from purplship.core.utils.serializable import Serializable, Deserializable


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[Element]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)

    def create_shipment(self, request: Serializable[Element]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}",
            data=bytearray(request.serialize(), "utf-8"),
            headers={"Content-Type": "application/xml"},
            method="POST",
        )
        return Deserializable(response, to_xml)
