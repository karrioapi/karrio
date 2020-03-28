"""PurplShip Sendle Tracking service mapper module."""

from typing import Tuple, List
from purplship.core.utils import Serializable, format_date, format_time
from purplship.core.models import TrackingRequest, Message, TrackingEvent, TrackingDetails
from pysendle.tracking import TrackingResponse
from purplship.carriers.sendle.error import parse_error_response
from purplship.carriers.sendle.utils import Settings


def parse_parcel_tracking_response(
    response: dict, settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    tracking: List[Tuple[str, TrackingResponse]] = [
        (p.get("ref"), TrackingResponse(**p.get("response")))
        for p in response
        if "tracking_events" in p.get("response")
    ]
    errors: List[dict] = [p.get("response") for p in response]
    return (
        [_extract_tracking(t, settings) for t in tracking],
        parse_error_response(errors, settings),
    )


def _extract_tracking(
    response: Tuple[str, TrackingResponse], settings: Settings
) -> TrackingDetails:
    tracking_number, detail = response
    return TrackingDetails(
        carrier=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            TrackingEvent(
                date=format_date(event.scan_time, '%Y-%m-%dT%H:%M:%SZ'),
                time=format_time(event.scan_time, '%Y-%m-%dT%H:%M:%SZ'),
                code=event.event_type,
                location=event.destination_location,
                description=event.description,
            )
            for event in detail.tracking_events
        ],
    )


def parcel_tracking_request(payload: TrackingRequest) -> Serializable[List[str]]:
    return Serializable(payload.tracking_numbers)
