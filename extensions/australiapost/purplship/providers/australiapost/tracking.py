from typing import List, Tuple
from australiapost_lib.track_item import (
    TrackingRequest as CarrierTrackingRequest,
    TrackingResult
)
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
from purplship.providers.australiapost.utils import Settings
from purplship.providers.australiapost.error import parse_error_response


def parse_tracking_response(response: dict, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details: List[TrackingResult] = response.get('tracking_results', [])
    tracking_details = [_extract_detail(detail, settings) for detail in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: TrackingResult, settings: Settings) -> TrackingDetails:
    item = detail.trackable_items[0]

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=detail.tracking_id,
        events=[
            TrackingEvent(
                date=DF.fdate(event.date, '%Y-%m-%dT%H:%M:%S%z'),
                description=event.description,
                location=event.location,
                time=DF.ftime(event.date, '%Y-%m-%dT%H:%M:%S%z'),
            ) for event in item.events
        ],
        delivered=(detail.status == 'Delivered')
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[CarrierTrackingRequest]:
    request = CarrierTrackingRequest(
        tracking_ids=payload.tracking_numbers
    )

    return Serializable(request, DP.to_dict)
