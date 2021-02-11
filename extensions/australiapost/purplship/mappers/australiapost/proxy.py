import urllib.parse
from purplship.core.utils import request as http, Serializable, Deserializable, DP
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.australiapost.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = http(
            url=f"{self.settings.server_url}/shipping/v1/track?{query}",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Account-Number": self.settings.account_number,
                "Authorization": f"Basic {self.settings.authorization}"
            },
            method="GET",
        )

        return Deserializable(response, DP.to_dict)
