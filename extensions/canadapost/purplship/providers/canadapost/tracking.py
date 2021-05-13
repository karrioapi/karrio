from typing import Tuple, List
from canadapost_lib.track import significant_events, occurrenceType
from purplship.providers.canadapost.utils import Settings
from purplship.core.utils import Element, Serializable, DF, XP, SF
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
    details = XP.find("tracking-detail", response)
    tracking_details: List[TrackingDetails] = [
        _extract_tracking(node, settings) for node in details
        if len(XP.find("occurrence", node)) > 0
    ]

    return tracking_details, parse_error_response(response, settings)


def _extract_tracking(detail_node: Element, settings: Settings) -> TrackingDetails:
    pin = XP.find("pin", detail_node, first=True)
    events: List[occurrenceType] = XP.find("occurrence", detail_node, occurrenceType)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=pin.text,
        events=[
            TrackingEvent(
                date=DF.fdate(event.event_date, "%Y-%m-%d"),
                time=DF.ftime(event.event_time, "%H:%M:%S"),
                code=event.event_identifier,
                location=SF.concat_str(event.event_site, event.event_province, join=True, separator=', '),
                description=event.event_description
            )
            for event in events
        ],
        delivered=any(e.event_identifier == "1496" for e in events)
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[str]]:
    return Serializable(payload.tracking_numbers)
