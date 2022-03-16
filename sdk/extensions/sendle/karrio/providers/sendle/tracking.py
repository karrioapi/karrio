from typing import List, Tuple
from sendle_lib.tracking_response import Tracking
from karrio.core.utils import (
    Serializable,
    DF,
    DP,
)
from karrio.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from karrio.providers.sendle.utils import Settings
from karrio.providers.sendle.error import parse_error_response


def parse_tracking_response(
    response: List[Tuple[str, dict]], settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    errors = [e for ref, e in response if "error" in e]
    tracking_details = [
        _extract_detail((ref, DP.to_object(Tracking, d)), settings)
        for ref, d in response
        if "tracking_events" in d
    ]

    return tracking_details, parse_error_response(errors, settings)


def _extract_detail(
    detail: Tuple[str, Tracking], settings: Settings
) -> TrackingDetails:
    tracking_number, tracking_details = detail
    estimated_delivery = (
        tracking_details.scheduling.estimated_delivery_date_minimum
        or tracking_details.scheduling.estimated_delivery_date_maximum
        or tracking_details.scheduling.delivered_on
    )

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        events=[
            TrackingEvent(
                date=DF.fdate(event.scan_time, "%Y-%m-%dT%H:%M:%SZ"),
                description=event.description,
                location=event.location,
                code=event.event_type,
                time=DF.ftime(event.scan_time, "%Y-%m-%dT%H:%M:%SZ"),
            )
            for event in reversed(tracking_details.tracking_events)
        ],
        estimated_delivery=DF.fdate(estimated_delivery, "%Y-%m-%d"),
        delivered=(tracking_details.state == "Delivered"),
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[list]:
    request = payload.tracking_numbers

    return Serializable(request)
