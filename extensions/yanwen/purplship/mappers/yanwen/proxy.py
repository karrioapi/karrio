import urllib.parse
from purplship.core.utils import DP, request as http, Serializable, Deserializable
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.yanwen.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = http(
            url=f"http://trackapi.yanwentech.com/api/tracking?{query}",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": self.settings.customer_number
            },
            method="GET",
        )

        return Deserializable(response, DP.to_dict)
