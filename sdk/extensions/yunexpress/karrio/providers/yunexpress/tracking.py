import time
from typing import List, Tuple
from yunexpress_lib.tracking import OrderInfo
from karrio.core.utils import (
    Serializable,
    SF,
    DP,
)
from karrio.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from karrio.providers.yunexpress.utils import Settings
from karrio.providers.yunexpress.error import parse_error_response


def parse_tracking_response(response: dict, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details = [_extract_detail(d, settings) for d in response.get('Items', [])]

    return details, parse_error_response(response, settings)


def _extract_detail(detail: dict, settings: Settings) -> TrackingDetails:
    order_info = DP.to_object(OrderInfo, detail)

    return TrackingDetails(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=order_info.TrackingNumber,
        events=[TrackingEvent(
            date=time.strftime('%Y-%m-%d'),
            description=order_info.msg
        )],
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[str]]:
    request = SF.concat_str(*payload.tracking_numbers, join=True, separator=',')

    return Serializable(request)
