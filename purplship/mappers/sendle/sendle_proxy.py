from typing import List, Union
from base64 import b64encode
import urllib.parse
from gds_helpers import request as http, to_dict, exec_parrallel
from purplship.domain.proxy import Proxy
from purplship.mappers.sendle.sendle_mapper import SendleMapper
from purplship.mappers.sendle.sendle_client import SendleClient
from pysendle.quotes import DomesticParcelQuote, InternationalParcelQuote

ParcelQuoteRequest = Union[DomesticParcelQuote, InternationalParcelQuote]


class SendleProxy(Proxy):
    def __init__(self, client: SendleClient, mapper: SendleMapper = None):
        self.client: SendleClient = client
        self.mapper: SendleMapper = SendleMapper(
            client
        ) if mapper is None else mapper

        pair = "%s:%s" % (self.client.sendle_id, self.client.api_key)
        self.authorization = b64encode(pair.encode("utf-8")).decode("ascii")

    """ Proxy interface methods """

    def get_quotes(self, parcel_quote_request: ParcelQuoteRequest) -> dict:
        query_string = urllib.parse.urlencode(to_dict(parcel_quote_request))
        response = http(
            url=f"{self.client.server_url}/quote?{query_string}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.authorization}",
            },
            method="GET",
        )
        return to_dict(response)

    def get_tracking(self, tracking_ids: List[str]) -> dict:

        def track(tracking_id):
            return {
                "ref": tracking_id,
                "response": to_dict(
                    http(
                        url=f"{self.client.server_url}/tracking/{tracking_id}",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Basic {self.authorization}",
                        },
                        method="GET",
                    )
                )
            }
        responses = exec_parrallel(track, tracking_ids)
        return responses
