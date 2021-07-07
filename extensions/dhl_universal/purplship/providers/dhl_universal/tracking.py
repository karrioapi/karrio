from typing import List, Tuple
from dhl_universal_lib.tracking import (
    TrackingRequest as DHLTrackingRequest,
)
from purplship.core.utils import (
    Serializable,
    DP,
    DF,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.dhl_universal.utils import Settings
from purplship.providers.dhl_universal.error import parse_error_response


def parse_tracking_response(response: List[dict], settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    errors = [e for e in response if 'shipments' not in e]
    details = [
        _extract_detail(d['shipments'][0], settings)
        for d in response if 'shipments' in d
    ]

    return details, parse_error_response(errors, settings)


def _extract_detail(detail: dict, settings: Settings) -> TrackingDetails:
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=str(detail.get('id')),
        events=[
            TrackingEvent(
                date=DF.fdate(event.get('timestamp'), '%Y-%m-%dT%H:%M:%S'),
                description=event.get('description'),
                location=(
                    event['location']['address'].get('addressLocality')
                    if event.get('location') is not None and event.get('location').get('address') is not None
                    else None
                ),
                code=event.get('statusCode'),
                time=DF.ftime(event.get('timestamp'), '%Y-%m-%dT%H:%M:%S'),
            ) for event in detail.get('events') or []
        ],
        delivered=(
            detail['status']['status'].lower() == "delivered"
            if all([detail['status'], detail['status']['status']]) else
            False
        )
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[DHLTrackingRequest]:
    request = [
        DHLTrackingRequest(
            trackingNumber=number,
            language="en",
        )
        for number in payload.tracking_numbers
    ]

    return Serializable(request, DP.to_dict)
