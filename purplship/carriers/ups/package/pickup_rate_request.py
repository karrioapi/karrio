from pyups.package_pickup import (
    PickupRateRequest
)
from purplship.core.utils.xml import Element
from purplship.core.models import PickupDetails, PickupRequest
from purplship.carriers.ups import Settings


def parse_pickup_rate_response(response: Element, settings: Settings) -> PickupDetails:
    pass


def pickup_rate_request(payload: PickupRequest, settings: Settings) -> PickupRateRequest:
    return PickupRateRequest(
        Request=None,
        PickupAddress=None,
        AlternateAddressIndicator=None,
        ServiceDateOption=None,
        PickupDateInfo=None,
        TaxInformationIndicator=None,
        UserLevelDiscountIndicator=None,
    )
