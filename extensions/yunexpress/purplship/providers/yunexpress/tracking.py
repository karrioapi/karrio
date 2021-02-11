import time
from typing import List, Tuple
from yunexpress_lib.tracking import OrderInfoType
from purplship.core.utils import (
    Element,
    Serializable,
    XP,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.yunexpress.utils import Settings
from purplship.providers.yunexpress.error import parse_error_response


def parse_tracking_response(response: Element, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details = response.xpath(".//*[local-name() = $name]", name="OrderInfo")
    tracking_details = [_extract_detail(detail, settings) for detail in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: Element, settings: Settings) -> TrackingDetails:
    item = XP.build(OrderInfoType, detail)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=item.TrackingNumber,
        events=[TrackingEvent(
            date=time.strftime('%Y-%m-%d'),
            description=item.msg
        )],
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[str]]:
    request = payload.tracking_numbers

    return Serializable(request)
