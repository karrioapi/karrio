from typing import List, Tuple
from asendia_us_lib.tracking_milestone_response import Datum as Tracking
from purplship.core.utils import (
    Serializable,
    DF,
    DP,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.asendia_us.utils import Settings
from purplship.providers.asendia_us.error import parse_error_response


def parse_tracking_response(response: List[dict], settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    tracking_details = [
        _extract_detail(detail["data"][0], settings)
        for detail in response if detail.get("data") is not None
    ]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: dict, settings: Settings) -> TrackingDetails:
    tracking = DP.to_object(Tracking, detail)
    delivered = (
        tracking.trackingMilestoneEvents[0].eventCode == 'Delivered'
        if len(tracking.trackingMilestoneEvents) > 0 else False
    )

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=tracking.trackingNumberVendor,
        events=[
            TrackingEvent(
                date=DF.fdate(event.eventOn, _date_format(event.eventOn)),
                time=DF.ftime(event.eventOn, _date_format(event.eventOn)),
                description=event.eventDescription,
                location=event.eventLocation,
                code=event.eventCode,
            )
            for event in tracking.trackingMilestoneEvents
        ],
        delivered=delivered
    )

def _date_format(date: str):
    return (
        '%Y-%m-%dT%H:%M:%S.%f%z'  if '.' in date else '%Y-%m-%dT%H:%M:%S%z'
    )



def tracking_request(payload: TrackingRequest, _) -> Serializable[list]:
    request = payload.tracking_numbers

    return Serializable(request)
