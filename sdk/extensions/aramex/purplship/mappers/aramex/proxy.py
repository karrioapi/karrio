from purplship.core.utils import XP, request as http, Serializable, Deserializable
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.aramex.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/ShippingAPI.V2/Tracking/Service_1_0.svc",
            data=bytearray(request.serialize(), "utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "soapAction": "http://ws.aramex.net/ShippingAPI/v1/Service_1_0/TrackShipments"
            },
            method="POST",
        )
        return Deserializable(response, XP.to_xml)
