from typing import Tuple, List
from canadapost_lib.track import pin_summary
from purplship.providers.canadapost.utils import Settings
from purplship.core.utils import Element, Serializable, DF, XP
from purplship.core.models import (
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
    Message,
)
from purplship.providers.canadapost.error import parse_error_response


def parse_tracking_response(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    pin_summaries = response.xpath(".//*[local-name() = $name]", name="pin-summary")
    tracking: List[TrackingDetails] = [
        _extract_tracking(pin, settings) for pin in pin_summaries
    ]
    return tracking, parse_error_response(response, settings)


def _extract_tracking(pin_summary_node: Element, settings: Settings) -> TrackingDetails:
    pin_summary_ = XP.build(pin_summary, pin_summary_node)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=pin_summary_.pin,
        events=[
            TrackingEvent(
                date=DF.fdate(pin_summary_.event_date_time, "%Y%m%d:%H%M%S"),
                time=DF.ftime(pin_summary_.event_date_time, "%Y%m%d:%H%M%S"),
                code=pin_summary_.event_type,
                location=pin_summary_.event_location,
                description=pin_summary_.event_description,
            )
        ],
        delivered=(pin_summary_.event_type == "DELIVERED")
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[str]]:
    return Serializable(payload.tracking_numbers)
