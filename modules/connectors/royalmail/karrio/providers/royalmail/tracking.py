from typing import List, Tuple
from karrio.schemas.royalmail.tracking import MailPieces
from karrio.core.models import (
    TrackingEvent,
    TrackingDetails,
    TrackingRequest,
    Message,
)
from karrio.providers.royalmail.utils import Settings
from karrio.providers.royalmail.error import parse_error_response
import karrio.lib as lib


def parse_tracking_response(
    _response: lib.Deserializable[List[dict]],
    settings: Settings,
) -> Tuple[List[TrackingDetails], List[Message]]:
    response = _response.deserialize()
    errors = [e for e in response if "mailPieces" not in e]
    details = [
        _extract_detail(d["mailPieces"], settings)
        for d in response
        if "mailPieces" in d
    ]

    return details, parse_error_response(errors, settings)


def _extract_detail(data: dict, settings: Settings) -> TrackingDetails:
    detail = lib.to_object(MailPieces, data)

    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=detail.mailPieceId,
        delivered=("Delivered" in detail.summary.lastEventName),
        events=[
            TrackingEvent(
                date=lib.fdate(event.eventDateTime, "%Y-%m-%dT%H:%M:%S%z"),
                description=event.eventName,
                location=event.locationName,
                code=event.eventCode,
                time=lib.flocaltime(event.eventDateTime, "%Y-%m-%dT%H:%M:%S%z"),
            )
            for event in detail.events
        ],
        estimated_delivery=lib.fdate(detail.estimatedDelivery.date, "%Y-%m-%d"),
    )


def tracking_request(payload: TrackingRequest, _) -> lib.Serializable:
    request = payload.tracking_numbers

    return lib.Serializable(request)
