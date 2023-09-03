from typing import List, Tuple
from karrio.schemas.royalmail.tracking import MailPieces
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
        _extract_detail(DP.to_object(MailPieces, d["mailPieces"]), settings)
        for d in response
        if "mailPieces" in d
    ]

    return details, parse_error_response(errors, settings)


def _extract_detail(detail: MailPieces, settings: Settings) -> TrackingDetails:
    return TrackingDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=detail.mailPieceId,
        delivered=("Delivered" in detail.summary.get("lastEventName")),
        events=[
            TrackingEvent(
                date=DF.fdate(event.eventDateTime, "%Y-%m-%dT%H:%M:%S%z"),
                description=event.eventName,
                location=event.locationName,
                code=event.eventCode,
                time=DF.ftime(event.eventDateTime, "%Y-%m-%dT%H:%M:%S%z"),
            )
            for event in detail.events
        ],
        estimated_delivery=DF.fdate(detail.estimatedDelivery.get("date"), "%Y-%m-%d"),
    )


def tracking_request(payload: TrackingRequest, _) -> Serializable:
    request = payload.tracking_numbers

    return Serializable(request)
