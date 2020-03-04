from typing import Tuple, List
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from pycaps.pickuprequest import PickupRequestDetailsType
from purplship.core.settings import Settings
from purplship.core.models import (
    Error, PickupDetails, PickupRequest
)


def parse_pickup_response(response: Element, settings: Settings) -> Tuple[PickupDetails, List[Error]]:
    pass


def _extract_pickup(response: Element, settings: Settings) -> PickupDetails:
    pass


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable[PickupRequestDetailsType]:
    request = PickupRequestDetailsType(
        pickup_type=None,
        pickup_location=None,
        contact_info=None,
        location_details=None,
        items_characteristics=None,
        pickup_volume=None,
        pickup_times=None,
        payment_info=None
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: PickupRequestDetailsType) -> str:
    return export(
        request,
        name_="pickup-request-details",
        namespacedef_='xmlns="http://www.canadapost.ca/ws/pickuprequest"',
    )
