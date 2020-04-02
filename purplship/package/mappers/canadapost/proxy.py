import base64
from typing import List
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.utils.helpers import (
    to_xml,
    request as http,
    exec_parrallel,
    bundle_xml,
)
from purplship.package.mappers.canadapost.settings import Settings
from purplship.package.proxy import Proxy as BaseProxy
from pycanadapost.shipment import ShipmentType
from pycanadapost.rating import mailing_scenario


class Proxy(BaseProxy):
    settings: Settings

    def get_rates(self, request: Serializable[mailing_scenario]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/rs/ship/price",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "application/vnd.cpc.ship.rate-v4+xml",
                "Accept": "application/vnd.cpc.ship.rate-v4+xml",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept-language": "en-CA",
            },
            method="POST",
        )
        return Deserializable(response, to_xml)

    def get_tracking(self, request: Serializable[List[str]]) -> Deserializable[str]:
        """
        get_tracking make parallel request for each pin
        """

        def track(tracking_pin: str) -> str:
            return http(
                url=f"{self.settings.server_url}/vis/track/pin/{tracking_pin}/summary",
                headers={
                    "Accept": "application/vnd.cpc.track+xml",
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept-language": "en-CA",
                },
                method="GET",
            )

        response: List[str] = exec_parrallel(track, request.serialize())

        return Deserializable(bundle_xml(xml_strings=response), to_xml)

    def create_shipment(
        self, request: Serializable[ShipmentType]
    ) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/rs/{self.settings.customer_number}/{self.settings.customer_number}/shipment",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "application/vnd.cpc.shipment-v8+xml",
                "Accept": "application/vnd.cpc.shipment-v8+xml",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept-language": "en-CA",
            },
            method="POST",
        )

        def fetch_label():
            url = next(
                (
                    link.get("href")
                    for link in to_xml(response).xpath(".//*[local-name() = $name]", name="link")
                    if link.get("rel") == "label"
                ),
                None
            )
            return http(
                decoder=lambda b: base64.encodebytes(b).decode('utf-8'),
                url=url,
                headers={
                    "Accept": "application/pdf",
                    "Authorization": f"Basic {self.settings.authorization}",
                },
                method="GET",
            ) if url else ""

        return Deserializable(bundle_xml([response, f"<label>{fetch_label()}</label>"]), to_xml)
