"""PurplShip Sendle Tracking service mapper module."""

from typing import Tuple, List
from purplship.core.utils.serializable import Serializable
from purplship.core.models import TrackingRequest, Error, TrackingEvent, TrackingDetails
from pysendle.tracking import TrackingResponse
from purplship.carriers.sendle.error import parse_error_response
from purplship.carriers.sendle.utils import Settings


def parse_parcel_tracking_response(
    response: dict, settings: Settings
) -> Tuple[List[TrackingDetails], List[Error]]:
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
        shipment_date=None,
        events=[
            TrackingEvent(
                date=event.scan_time,
                signatory=None,
                code=event.event_type,
                location=event.destination_location,
                description=event.description,
            )
            for event in detail.tracking_events
        ],
    )


def parcel_tracking_request(payload: TrackingRequest) -> Serializable[List[str]]:
    return Serializable(payload.tracking_numbers)
