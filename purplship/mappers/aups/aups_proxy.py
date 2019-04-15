import urllib.parse
from typing import List, Union, Type, cast
from base64 import b64encode
from gds_helpers import request as http, jsonify, to_dict
from purplship.mappers.aups.aups_logistic_mapper import AustraliaPostMapper as AustraliaPostLogisticMapper
from purplship.mappers.aups.aups_postage_mapper import AustraliaPostMapper as AustraliaPostPostageMapper
from purplship.mappers.aups.aups_client import AustraliaPostClient, AustraliaPostApi
from purplship.domain.proxy import Proxy
from pyaups.shipping_price_request import ShippingPriceRequest
from pyaups.domestic_letter_postage import ServiceRequest as DomesticLetterServiceRequest
from pyaups.international_letter_postage import ServiceRequest as IntlLetterServiceRequest
from pyaups.domestic_parcel_postage import ServiceRequest as DomesticParcelServiceRequest
from pyaups.international_parcel_postage import ServiceRequest as IntlParcelServiceRequest

Mapper = Union[AustraliaPostLogisticMapper, AustraliaPostPostageMapper]
PostageRequest = Union[
    DomesticLetterServiceRequest,
    DomesticParcelServiceRequest,
    IntlLetterServiceRequest,
    IntlParcelServiceRequest
]
MAPPERS = {
    AustraliaPostApi.Logistic: AustraliaPostLogisticMapper,
    AustraliaPostApi.Postage: AustraliaPostPostageMapper
}


class AustraliaPostProxy(Proxy):
    def __init__(self, client: AustraliaPostClient, mapper: Mapper = None):
        self.client: AustraliaPostClient = client
        self.mapper: Mapper = cast(
            Mapper, mapper or MAPPERS[AustraliaPostApi(client.api)](client)
        )
        self.authorization = b64encode(
            f"{self.client.api_key}:{self.client.password}".encode("utf-8")
        ).decode("ascii") if self.client.password else None

    """ Proxy interface methods """

    def get_quotes(self, request: Union[ShippingPriceRequest, Type[PostageRequest]]) -> dict:
        response = (
            self._get_shipping_price
            if isinstance(request, ShippingPriceRequest) else
            self._get_postage_service
        )(request)
        return to_dict(response)

    def get_tracking(self, tracking_ids: List[str]) -> dict:
        ids = ','.join(tracking_ids)
        result = http(
            url=f"{self.client.server_url}/shipping/v1/track?tracking_ids={ids}",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Account-Number": self.client.account_number,
                "Authorization": f"Basic {self.authorization}",
            },
            method="GET",
        )
        return to_dict(result)

    """ Private methods """

    def _get_shipping_price(self, shipping_price_request: ShippingPriceRequest) -> str:
        data = jsonify(to_dict(shipping_price_request))
        return http(
            url=f"{self.client.server_url}/shipping/v1/prices/shipments",
            data=bytearray(data, "utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Account-Number": self.client.account_number,
                "Authorization": f"Basic {self.authorization}",
            },
            method="POST",
        ).replace('from', 'from_')

    def _get_postage_service(self, postage_request: PostageRequest) -> str:
        route: str = {
            DomesticParcelServiceRequest: "/parcel/domestic/service.json",
            DomesticLetterServiceRequest: "/letter/domestic/service.json",
            IntlParcelServiceRequest: "/parcel/international/service.json",
            IntlLetterServiceRequest: "/letter/international/service.json",
        }[type(postage_request)]
        query_string = urllib.parse.urlencode(to_dict(postage_request))
        return http(
            url=f"{self.client.server_url}/postage{route}?{query_string}",
            headers={
                "Content-Type": "application/json",
                "AUTH-KEY": self.client.api_key,
            },
            method="GET",
        )
