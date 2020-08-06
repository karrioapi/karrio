from typing import Tuple, List
from pycanadapost.track import pin_summary
from purplship.providers.canadapost.utils import Settings
from purplship.core.utils import Element, Serializable, format_date, format_time
from purplship.core.models import (
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
    Message,
)
from purplship.providers.canadapost.error import parse_error_response


def parse_tracking_summary(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    pin_summaries = response.xpath(".//*[local-name() = $name]", name="pin-summary")
    tracking: List[TrackingDetails] = [
        _extract_tracking(pin, settings) for pin in pin_summaries
    ]
    return tracking, parse_error_response(response, settings)


def _extract_tracking(pin_summary_node: Element, settings: Settings) -> TrackingDetails:
    pin_summary_ = pin_summary()
    pin_summary_.build(pin_summary_node)
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=pin_summary_.pin,
        events=[
            TrackingEvent(
                date=format_date(pin_summary_.event_date_time, "%Y%m%d:%H%M%S"),
                time=format_time(pin_summary_.event_date_time, "%Y%m%d:%H%M%S"),
                signatory=pin_summary_.signatory_name,
                code=pin_summary_.event_type,
                location=pin_summary_.event_location,
                description=pin_summary_.event_description,
            )
        ],
    )


def tracking_pins_request(payload: TrackingRequest) -> Serializable[List[str]]:
    return Serializable(payload.tracking_numbers)
