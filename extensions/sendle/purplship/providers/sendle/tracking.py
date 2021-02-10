from typing import List, Tuple
from sendle_lib.tracking import TrackingResponse
from purplship.core.utils import (
    Serializable,
    DF,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.sendle.utils import Settings
from purplship.providers.sendle.error import parse_error_response


def parse_tracking_response(response: List[dict], settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    errors = [e for e in response if 'error' in e]
    tracking_details = [
        _extract_detail(TrackingResponse(**d), settings)
        for d in response if 'tracking_details' in d
    ]

    return tracking_details, parse_error_response(errors, settings)


def _extract_detail(detail: TrackingResponse, settings: Settings) -> TrackingDetails:
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=detail.tracking_number,
        events=[
            TrackingEvent(
                date=DF.fdate(event.scan_time, '%Y-%m-%dT%H:%M:%SZ'),
                description=event.description,
                location=event.location,
                code=event.event_type,
                time=DF.fdate(event.scan_time, '%Y-%m-%dT%H:%M:%SZ'),
            )
            for event in detail.tracking_details.tracking_events
        ],
        delivered=(detail.tracking_details.state == 'Delivered')
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[list]:
    return Serializable(payload.tracking_numbers)
