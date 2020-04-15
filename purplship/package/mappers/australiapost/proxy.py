from typing import List, Union
from purplship.core.utils.helpers import request as http, to_dict
from purplship.core.utils.serializable import Deserializable, Serializable
from purplship.package.mappers.australiapost.settings import Settings
from purplship.package.proxy import Proxy as BaseProxy
from pyaustraliapost.shipping_price_request import ShippingPriceRequest
from pyaustraliapost.domestic_letter_postage import (
    ServiceRequest as DomesticLetterServiceRequest,
)
from pyaustraliapost.international_letter_postage import (
    ServiceRequest as IntlLetterServiceRequest,
)
from pyaustraliapost.domestic_parcel_postage import (
    ServiceRequest as DomesticParcelServiceRequest,
)
from pyaustraliapost.international_parcel_postage import (
    ServiceRequest as IntlParcelServiceRequest,
)

PostageRequest = Union[
    DomesticLetterServiceRequest,
    DomesticParcelServiceRequest,
    IntlLetterServiceRequest,
    IntlParcelServiceRequest,
]


class Proxy(BaseProxy):
    settings: Settings

    """ Proxy interface methods """

    def get_rates(
        self, request: Serializable[ShippingPriceRequest]
    ) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/shipping/v1/prices/shipments",
            data=bytearray(request.serialize().replace("from_", "from"), "utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Account-Number": self.settings.account_number,
                "Authorization": f"Basic {self.settings.authorization}",
            },
            method="POST",
        ).replace("from", "from_")
        return Deserializable(response, to_dict)

    def get_tracking(self, request: Serializable[List[str]]) -> Deserializable[str]:
        response = http(
            url=f"{self.settings.server_url}/shipping/v1/track?tracking_ids={request.serialize()}",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Account-Number": self.settings.account_number,
                "Authorization": f"Basic {self.settings.authorization}",
            },
            method="GET",
        )
        return Deserializable(response, to_dict)
