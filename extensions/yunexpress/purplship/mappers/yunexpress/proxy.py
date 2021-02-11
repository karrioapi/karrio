from typing import List
from purplship.core.utils import XP, request as http, Serializable, Deserializable, exec_async
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.yunexpress.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable:

        def _get_tracking(tracking_number: str):
            return http(
                url=f"{self.settings.server_url}/WayBill/GetTrackingNumber?trackingNumber={tracking_number}",
                headers={
                    'Authorization': f"basic {self.settings.authorization}",
                    'Content-Type': "application/xml; charset=utf8",
                    'Accept': "application/xml",
                    'Accept-Language': "en-us"
                },
                method="GET",
            )

        responses: List[str] = exec_async(_get_tracking, request.serialize())
        return Deserializable(XP.bundle_xml(xml_strings=responses), XP.to_xml)
