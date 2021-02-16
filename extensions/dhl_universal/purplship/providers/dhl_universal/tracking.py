from typing import List, Tuple
from dhl_universal_lib.tracking import (
    TrackingRequest as DHLTrackingRequest,
    Shipment,
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
        _extract_detail(Shipment(**d['shipments'][0]), settings)
        for d in response if 'shipments' in d
    ]

    return details, parse_error_response(errors, settings)


def _extract_detail(detail: Shipment, settings: Settings) -> TrackingDetails:
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        tracking_number=str(detail.id),
        events=[
            TrackingEvent(
                date=DF.fdate(event.timestamp, '%Y-%m-%dT%H:%M:%S'),
                description=event.description,
                location=(
                    event.location.address.addressLocality
                    if event.location is not None and event.location.address is not None
                    else None
                ),
                code=event.statusCode,
                time=DF.ftime(event.timestamp, '%Y-%m-%dT%H:%M:%S'),
            ) for event in detail.events
        ],
        delivered=detail.status.status.lower() == "delivered"
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
