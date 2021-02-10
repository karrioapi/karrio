from typing import List, Tuple
from dhl_universal_lib.tracking import (
    TrackingRequest as DHLTrackingRequest,
    Shipment,
)
from purplship.core.utils import (
    Serializable,
    DP,
    DF,
    SF,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from purplship.providers.dhl_universal.utils import Settings
from purplship.providers.dhl_universal.error import parse_error_response


def parse_tracking_response(response, settings: Settings) -> Tuple[List[TrackingDetails], List[Message]]:
    details: List[dict] = response.get('shipments')
    tracking_details = [_extract_detail(Shipment(**d), settings) for d in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail: Shipment, settings: Settings) -> TrackingDetails:
    return TrackingDetails(
        carrier_name=settings.dhl_universal,
        carrier_id=settings.dhl_universal_id,

        tracking_number=detail.id,
        events=[
            TrackingEvent(
                date=DF.fdate(event.timestamp, '%Y-%m-%dT%H:%M:%S'),
                description=event.description,
                location=SF.concat_str(
                    event.location.address.countryCode,
                    event.location.address.postalCode,
                    event.location.address.addressLocality,
                    join=True
                ),
                code=event.status,
                time=DF.ftime(event.timestamp, '%Y-%m-%dT%H:%M:%S'),
            ) for event in detail.events
        ],
        delivered=detail.status.status == "DELIVERED"
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
