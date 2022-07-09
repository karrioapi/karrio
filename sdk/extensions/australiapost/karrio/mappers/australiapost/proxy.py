import urllib.parse
from karrio.core.utils import request as http, Serializable, Deserializable, DP
from karrio.api.proxy import Proxy as BaseProxy
from karrio.mappers.australiapost.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable[str]:
        query = urllib.parse.urlencode(request.serialize())
        response = http(
            url=f"{self.settings.server_url}/shipping/v1/track?{query}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Account-Number": self.settings.account_number,
                "Authorization": f"Basic {self.settings.authorization}",
            },
        )

        return Deserializable(response, DP.to_dict)
