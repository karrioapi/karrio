import urllib.parse
from typing import List
from purplship.core.utils import DP, request as http, Serializable, Deserializable, exec_async
from purplship.api.proxy import Proxy as BaseProxy
from purplship.mappers.dhl_universal.settings import Settings


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy Methods """

    def get_tracking(self, request: Serializable) -> Deserializable[str]:

        def _get_tracking(tracking_request: dict):
            query = urllib.parse.urlencode(tracking_request)
            return http(
                url=f"{self.settings.server_url}/track/shipments?{query}",
                headers={
                    "Accept": "application/json",
                    "DHL-API-Key": self.settings.consumer_key
                },
                method="GET",
            )

        responses: List[dict] = exec_async(_get_tracking, request.serialize())
        return Deserializable(responses, lambda res: [DP.to_dict(r) for r in res])
