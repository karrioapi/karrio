from typing import List, Tuple
from ups_lib.rest_tracking_response import (
    Shipment,
    Package,
)
from purplship.core.utils import (
    Serializable,
    Envelope,
    DP,
    DF,
    SF,
)
from purplship.core.models import (
    TrackingEvent,
    TrackingRequest,
    TrackingDetails,
    Message,
)
from purplship.providers.ups.error import parse_rest_error_response
from purplship.providers.ups.utils import Settings


def parse_tracking_response(
    responses: List[Tuple[str, dict]], settings: Settings
) -> Tuple[List[TrackingDetails], List[Message]]:
    details = [
        _extract_details(response["trackResponse"]["shipment"][0], settings)
        for _, response in responses
        if "trackResponse" in response
    ]
    messages = [
        parse_rest_error_response(
            response["response"]["errors"],
            settings,
            details=dict(tracking_number=tracking_number),
        )
        for tracking_number, response in responses
        if "response" in response
    ]

    return details, messages


def _extract_details(detail: dict, settings: Settings) -> TrackingDetails:
    package: Package = next(iter(DP.to_object(Shipment, detail).package))
    delivered = any(a.status.type == "D" for a in package.activity)
    estimated_delivery = next(
        iter([d.date for d in package.deliveryDate if d.type == "DEL"]), None
    )

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=package.trackingNumber,
        events=[
            TrackingEvent(
                date=DF.fdate(a.date, "%Y%m%d"),
                description=a.status.description if a.status else None,
                location=(
                    SF.concat_str(
                        a.location.address.city,
                        a.location.address.stateProvince,
                        a.location.address.postalCode,
                        a.location.address.country,
                        join=True,
                        separator=", ",
                    )
                    if a.location
                    else None
                ),
                time=DF.ftime(a.time, "%H%M%S"),
                code=a.status.code if a.status else None,
            )
            for a in package.activity
        ],
        delivered=delivered,
        estimated_delivery=DF.fdate(estimated_delivery, "%Y%m%d"),
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable[List[Envelope]]:
    return Serializable(payload.tracking_numbers)
