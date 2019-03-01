from typing import List
from base64 import b64encode
from gds_helpers import request as http, jsonify, to_dict
from purplship.mappers.aups.aups_mapper import AustraliaPostMapper
from purplship.mappers.aups.aups_client import AustraliaPostClient
from purplship.domain.proxy import Proxy
from pyaups.shipping_price_request import ShippingPriceRequest


class AustraliaPostProxy(Proxy):
    def __init__(self, client: AustraliaPostClient, mapper: AustraliaPostMapper = None):
        self.client: AustraliaPostClient = client
        self.mapper: AustraliaPostMapper = AustraliaPostMapper(
            client
        ) if mapper is None else mapper

        pair = "%s:%s" % (self.client.username, self.client.password)
        self.authorization = b64encode(pair.encode("utf-8")).decode("ascii")

    """ Proxy interface methods """

    def get_quotes(self, shipping_price_request: ShippingPriceRequest) -> dict:
        data = jsonify(to_dict(shipping_price_request))
        result = http(
            url=f"{self.client.server_url}/prices/shipments",
            data=bytearray(data, "utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Account-Number": self.client.account_number,
                "Authorization": f"Basic {self.authorization}",
            },
            method="POST",
        )
        return to_dict(result)

    def get_trackings(self, tracking_ids: List[str]) -> dict:
        ids = ','.join(tracking_ids)

        result = http(
            url=f"{self.client.server_url}/track?tracking_ids={ids}",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Account-Number": self.client.account_number,
                "Authorization": f"Basic {self.authorization}",
            },
            method="GET",
        )
        return to_dict(result)
