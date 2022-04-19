from typing import List, Tuple
from dhl_universal_lib.tracking import TrackingRequest as DHLTrackingRequest, Shipment
from karrio.core.utils import (
    Serializable,
    DP,
    DF,
)
from karrio.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from karrio.providers.dhl_universal.utils import Settings
from karrio.providers.dhl_universal.error import parse_error_response

date_formats = [
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S.%f%z",
]


def parse_tracking_response(
    response: List[dict], settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    errors = [e for e in response if "shipments" not in e]
    details = [
        _extract_detail(DP.to_object(Shipment, d["shipments"][0]), settings)
        for d in response
        if "shipments" in d
    ]

    return details, parse_error_response(errors, settings)


def _extract_detail(detail: Shipment, settings: Settings) -> TrackingDetails:
    delivered = (getattr(detail.status, "statusCode", None) or "") == "delivered" or (
        getattr(detail.status, "status", None) or ""
    ).lower() == "delivered"
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=str(detail.id),
        events=[
            TrackingEvent(
                date=DF.fdate(event.timestamp, try_formats=date_formats),
                description=event.description or event.status or " ",
                location=(
                    event.location.address.addressLocality
                    if event.location is not None and event.location.address is not None
                    else None
                ),
                code=event.statusCode or "",
                time=DF.ftime(event.timestamp, try_formats=date_formats),
            )
            for event in detail.events or []
        ],
        estimated_delivery=DF.fdate(
            detail.estimatedTimeOfDelivery, try_formats=date_formats
        ),
        delivered=delivered,
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
