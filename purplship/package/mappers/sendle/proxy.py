import urllib.parse
from typing import List, Union
from purplship.core.utils.serializable import Deserializable, Serializable
from purplship.core.utils.helpers import request as http, to_dict, exec_parrallel
from purplship.package.proxy import Proxy as BaseProxy
from purplship.package.mappers.sendle.settings import Settings
from pysendle.quotes import DomesticParcelQuote, InternationalParcelQuote

ParcelQuoteRequest = Union[DomesticParcelQuote, InternationalParcelQuote]


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy interface methods """

    def get_rates(
        self, request: Serializable[ParcelQuoteRequest]
    ) -> Deserializable[str]:
        query_string = urllib.parse.urlencode(request.serialize())
        response = http(
            url=f"{self.settings.server_url}/quote?{query_string}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
            },
            method="GET",
        )
        return Deserializable(response, to_dict)

    def get_tracking(
        self, request: Serializable[List[str]]
    ) -> Deserializable[List[dict]]:
        def track(tracking_id):
            return {
                "ref": tracking_id,
                "response": to_dict(
                    http(
                        url=f"{self.settings.server_url}/tracking/{tracking_id}",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Basic {self.settings.authorization}",
                        },
                        method="GET",
                    )
                ),
            }

        responses: List[dict] = exec_parrallel(track, request.serialize())
        return Deserializable(responses)
