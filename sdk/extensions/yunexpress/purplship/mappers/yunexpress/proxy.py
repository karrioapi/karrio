from purplship.core.utils import DP, request as http, Serializable, Deserializable
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.yunexpress.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable:
        response = http(
            url=f"{self.settings.server_url}/WayBill/GetTrackingNumber?trackingNumber={request.serialize()}",
            headers={
                'Authorization': f"basic {self.settings.authorization}",
                'Accept': "application/json",
                'Accept-Language': "en-us"
            },
            method="GET",
        )

        return Deserializable(response, DP.to_dict)
